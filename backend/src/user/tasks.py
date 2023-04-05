import hashlib
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from . import models


def search(db: Session):
    return paginate(db.query(models.User))


def find(db: Session, model_id: str):
    return db.query(models.User).filter(models.User.id == model_id).first()


def find_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def delete(db: Session, model_id):
    connection = db.query(models.User).filter(models.User.id == model_id).one_or_none()
    if connection is None:
        return None
    db.delete(connection)
    db.commit()
    return True


def get_access_token(db: Session, token: str):
    model_id, token = token.split("|")
    instance = db.query(models.AccessToken).filter(models.AccessToken.id == model_id).first()
    if instance is None:
        return None
    elif instance.token != hashlib.sha256(token.encode()).hexdigest():
        return None
    return instance


def put_access_token(db: Session, user_id: int, token: str):
    model = models.AccessToken(user_id=user_id, token=token)
    db.add(model)
    db.commit()
    return model
