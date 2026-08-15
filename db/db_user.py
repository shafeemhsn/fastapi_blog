from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.hash import Hash
from db.models import DbUser
from schemas import UserBase


def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_user(db: Session):
    return db.query(DbUser).all()

def get_user(db: Session, id: int):
    user = db.get(DbUser, id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} was not found"
        )
    return user

def get_user_username(db: Session, username: str):
    user = (
        db.query(DbUser)
        .filter(DbUser.username == username)
        .first()
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with username {username} was not found"
        )
    return user

def update_user(db: Session, id: int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} was not found"
        )
    user.update({
        DbUser.username: request.username,
        DbUser.email: request.email,
        DbUser.password: Hash.bcrypt(request.password)

    })
    db.commit()
    return 'ok'

def delete_user(db: Session, id: int):
    user = get_user(db, id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} was not found"
        )
    db.delete(user)
    db.commit()
    return 'ok'