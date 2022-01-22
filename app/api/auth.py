import logging
from fastapi import APIRouter, status, Depends, HTTPException, Body, BackgroundTasks, Response
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud
from app.schemas import _user, _assets
from app.api.deps import get_current_user, get_db
from app.core import JWTSettings, settings
from app.utils import send_email_verification, send_password_reset


@AuthJWT.load_config
def get_config():
    return JWTSettings()


logger = logging.getLogger('main')
router = APIRouter()


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def Create_User(
        user_in: _user.UserCreate,
        Authorize: AuthJWT = Depends(),
        db: Session = Depends(get_db)):

    response = []

    # Check if user with given credentials exists
    if crud.user.get_by_username(db, user_in.username):
        response.append(Responses.username_taken)
    elif crud.user.get_by_email(db, user_in.email):
        response.append(Responses.email_taken)

    # Throw errors if user already exists
    if len(response) > 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=response
        )
    # Create user
    try:
        user = crud.user.create(db, obj_in=user_in)
        logger.info(f'{user.username} created an account.')
    except Exception as e:
        logger.error(f'/register: {e}')

    # Authenticate to validate registration
    user = crud.user.authenticate(db, user_in.email, user_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=Responses.login_fail
        )

    # Create the tokens and passing to set_access_cookies or set_refresh_cookies
    access_token = Authorize.create_access_token(subject=user.id)
    refresh_token = Authorize.create_refresh_token(subject=user.id)

    # Set the JWT and CSRF double submit cookies in the response
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)

    return {'message': 'Account created successfully.'}


@router.post('/login')
async def login(
        user: _user.UserLogin,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    user = crud.user.authenticate(db, user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=Responses.login_fail
        )
    # Create the tokens and passing to set_access_cookies or set_refresh_cookies
    access_token = Authorize.create_access_token(subject=user.id)
    refresh_token = Authorize.create_refresh_token(subject=user.id)
    # Set the JWT and CSRF double submit cookies in the response

    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return {"message": "Successfully logged in."}


@router.delete('/logout')
async def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"message": "Successfully logged out."}


@router.get('/refresh')
async def Refresh_Token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required(csrf_token=None)
    
    user_id = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=user_id)
    
    Authorize.set_access_cookies(access_token)
    
    return {}


@router.get('/send_verification')
async def Send_Email_Verification(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    db_user = get_current_user(db, Authorize)

    if db_user.is_verified:
        return {'message': 'Email account is verified.'}

    db_user_verify = crud.user.generate_code(db, user_id=db_user.id)

    if db_user_verify.times_generated >= 10:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    theme = crud.theme.get(db, db_user.theme_id)
    email = _assets.Email(
        email=[db_user.email],
        body={
            'code': db_user_verify.code,
            'theme': jsonable_encoder(theme)
        })

    await send_email_verification(email, db_user)
    
    return {'message': f'Email verification sent. {db_user_verify.times_generated} / 10.'}


@router.post('/verify_email')
async def Verify_Email(
        code: str = Body(..., embed=True),
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    db_user = get_current_user(db, Authorize)

    if db_user.is_verified:
        return {'message': 'Email account is verified.'}

    code_verified = crud.user.verify_code(db, code=code, user_id=db_user.id)
    if not code_verified:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=Responses.invalid_code
        )

    return {'message': 'Email account verified successfully.'}


@router.post('/send_password_reset')
async def Send_Password_Reset(
        background_tasks: BackgroundTasks,
        email: EmailStr = Body(..., embed=True),
        db: Session = Depends(get_db)):

    db_user = crud.user.get_by_email(db, email)
    if not db_user:
        return Response(status_code=status.HTTP_200_OK)

    db_pass_reset = crud.user.new_password_reset(db, db_user)
    if db_pass_reset.suspended:
        return Response(status_code=status.HTTP_200_OK)

    theme = crud.theme.get(db, db_user.theme_id)
    email = _assets.Email(
        email=[db_user.email],
        body={
            'url': f'{settings.URL_FE}/reset_password/{db_pass_reset.uri}',
            'theme': jsonable_encoder(theme)
        })
    send_password_reset(email, db_user, background_tasks)
    return Response(status_code=status.HTTP_200_OK)


@router.post('/reset_password/{uri}')
async def Reset_Passwords_Via_Email(
        uri: str,
        passwords: _user.ResetPasswords,
        db: Session = Depends(get_db)):

    if not crud.user.reset_password(db, passwords, uri):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_200_OK)


class Responses(object):
    username_taken = {
        "loc": [
            "body",
            "username"
        ],
        "msg": "Username is taken."
    }

    email_taken = {
        "loc": [
            "body",
            "email"
        ],
        "msg": "Email is taken."
    }

    login_fail = [
        {
            "loc": [
                "body",
                "email"
            ],
            "msg": "Incorect email or password."
        },
        {
            "loc": [
                "body",
                "password"
            ],
            "msg": "Incorect email or password."
        }
    ]

    invalid_code = [
        {
            "loc": [
                "body",
                "code"
            ],
            "msg": "Code is invalid."
        }
    ]
