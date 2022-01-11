from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password_w_salt: str, hashed_password: str):
    return pwd_context.verify(plain_password_w_salt, hashed_password)


def get_password_hash(password_w_salt):
    return pwd_context.hash(password_w_salt)
