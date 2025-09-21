from sqlalchemy.orm import Session
from . import models

def get_user(db: Session, uid: str):
    return db.query(models.User).filter(models.User.uid == uid).first()

def upsert_user(db: Session, uid: str, email: str | None = None):
    user = get_user(db, uid)
    if not user:
        user = models.User(uid=uid, email=email)
        db.add(user)
    else:
        if email:
            user.email = email
    db.commit()
    db.refresh(user)
    return user

def consume_free_hq(db: Session, uid: str):
    user = get_user(db, uid)
    if not user:
        return None
    if not user.has_used_free_hq:
        user.has_used_free_hq = True
        db.commit()
        db.refresh(user)
    return user

def set_subscriber(db: Session, uid: str, is_subscriber: bool):
    user = get_user(db, uid)
    if not user:
        return None
    user.is_subscriber = is_subscriber
    db.commit()
    db.refresh(user)
    return user
