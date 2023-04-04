import hashlib
from sqlalchemy.orm import Session
from .models import User, AccessToken


def get_user_by_id(db: Session, model_id: str):
    return db.query(User).filter(User.id == model_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_access_token(db: Session, token: str):
    model_id, token = token.split("|")
    instance = db.query(AccessToken).filter(AccessToken.id == model_id).first()
    if instance is None:
        return None
    elif instance.token != hashlib.sha256(token.encode()).hexdigest():
        return None
    return instance


def put_access_token(db: Session, user_id: int, token: str):
    instance = AccessToken(user_id=user_id, token=token)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance
