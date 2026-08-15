from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.oauth2 import get_current_user
from db import db_user
from db.database import get_db
from schemas import UserBase, UserDisplay

router = APIRouter(prefix="/user", tags=["user"])

DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[UserBase, Depends(get_current_user)]


@router.post("/", response_model=UserDisplay)
def create_user(request: UserBase, db: DbSession):
    return db_user.create_user(db, request)


@router.get("/", response_model=list[UserDisplay])
def get_all_users(db: DbSession, current_user: CurrentUser):
    return db_user.get_all_user(db)


@router.get("/{id}", response_model=UserDisplay)
def get_user(id: int, db: DbSession, current_user: CurrentUser):
    return db_user.get_user(db, id)


@router.post("/{id}/update")
def update_user(id: int, request: UserBase, db: DbSession, current_user: CurrentUser):
    return db_user.update_user(db, id, request)


@router.delete("/{id}")
def delete_user(id: int, db: DbSession):
    return db_user.delete_user(db, id)
