import hashlib
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .schemas import UserCreate
from .models import User, AccessToken


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def search(db: Session):
    return paginate(db.query(User))


def find(db: Session, model_id: int):
    return db.query(User).filter(User.id == model_id).first()


def find_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create(db: Session, item: UserCreate):
    model = User(
        name=item.name,
        username=item.username,
        password=pwd_context.encrypt(item.password),
        state=item.state
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def update(db: Session, model_id, item: UserCreate):
    model = db.query(User).filter(User.id == model_id).one_or_none()
    if model is None:
        return None
    model.name = item.name
    model.state = item.state
    db.commit()
    db.refresh(model)
    return model


def delete(db: Session, model_id):
    model = db.query(User).filter(User.id == model_id).one_or_none()
    if model is None:
        return None
    db.delete(model)
    db.commit()
    return True


def get_access_token(db: Session, token: str):
    model_id, token = token.split("|")
    model = db.query(AccessToken).filter(AccessToken.id == model_id).first()
    if model is None:
        return None
    elif model.token != hashlib.sha256(token.encode()).hexdigest():
        return None
    return model


def put_access_token(db: Session, user_id: int, token: str):
    model = AccessToken(user_id=user_id, token=token)
    db.add(model)
    db.commit()
    db.refresh(model)
    return model
