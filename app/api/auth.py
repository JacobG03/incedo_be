import logging
from fastapi import APIRouter, status, Depends, HTTPException, Body
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api.deps import get_db
from app.core import JWTSettings
from app.utils import send_email_verification


@AuthJWT.load_config
def get_config():
    return JWTSettings()


logger = logging.getLogger('main')
router = APIRouter()


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def Create_User(
        user_in: schemas.UserCreate,
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
def login(
        user: schemas.UserLogin,
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
def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"message": "Successfully logged out."}


@router.get('/verify_email')
async def Send_Email_Verification(
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    Authorize.jwt_required()
    db_user = crud.user.get(db, model_id=Authorize.get_jwt_subject())
    
    if db_user.is_verified:
        return {'message': 'Email account is verified.'}

    db_user_verify = crud.user.generate_code(db, user_id=db_user.id)

    email = schemas.Email(email=[db_user.email], body={
                          'code': db_user_verify.code})
    await send_email_verification(email)

    return {'message': 'Email verification sent.'}


@router.post('/verify_email')
async def Verify_Email_Account(
        code: str = Body(..., embed=True),
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):

    Authorize.jwt_required()
    db_user = crud.user.get(db, model_id=Authorize.get_jwt_subject())
    
    if db_user.is_verified:
        return {'message': 'Email account is verified.'}

    code_verified = crud.user.verify_code(db, code=code, user_id=db_user.id)
    if not code_verified:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=Responses.invalid_code
        )

    return {'message': 'Email account verified successfully.'}


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
