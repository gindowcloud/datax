import hashlib
import random
import string
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .database import get_db
from .user.tasks import find, find_by_username, put_access_token, get_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 用户认证
def authenticate(db: Session, username: str, password: str):
    user = find_by_username(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    plain = ''.join(random.sample(string.ascii_letters, 40))
    token = hashlib.sha256(plain.encode()).hexdigest()
    access_token = put_access_token(db, user.id, token)
    return str(access_token.id)+'|'+plain


# 认证用户
def session(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="认证失败")
    access_token = get_access_token(db, token)
    if access_token is None:
        raise credentials_exception
    else:
        user = find(db, access_token.user_id)
        if user is None:
            raise credentials_exception
    return user
