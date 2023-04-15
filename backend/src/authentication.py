import hashlib
import random
import string
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .database import get_db
from .response import error
from .errors import ERROR_USER_NOT_FOUND, ERROR_USER_WRONG_PASSWORD, ERROR_USER_TOKEN_EXPIRED
from .user.models import User
from .user.curd import find, find_by_username, put_access_token, get_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 用户认证
def authenticate(db: Session, username: str, password: str):
    user = find_by_username(db, username)
    if not user:
        raise error(ERROR_USER_NOT_FOUND)
    if not pwd_context.verify(password, user.password):
        raise error(ERROR_USER_WRONG_PASSWORD)
    plain = ''.join(random.sample(string.ascii_letters, 40))
    token = hashlib.sha256(plain.encode()).hexdigest()
    access_token = put_access_token(db, user.id, token)
    return str(access_token.id)+'|'+plain


# 认证用户
def session(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    access_token = get_access_token(db, token)
    if access_token is None:
        raise error(ERROR_USER_TOKEN_EXPIRED)
    else:
        user = find(db, access_token.user_id)
        if user is None:
            raise error(ERROR_USER_NOT_FOUND)
    return user


# 修改密码
def password(db: Session, user: User, password: str, newpassword: str):
    if not pwd_context.verify(password, user.password):
        raise error(ERROR_USER_WRONG_PASSWORD)
    user.password = pwd_context.encrypt(newpassword)
    db.commit()
    db.refresh(user)
    return user


# 修改资料
def settings(db: Session, user: User, name: str):
    user.name = name
    db.commit()
    db.refresh(user)
    return user
