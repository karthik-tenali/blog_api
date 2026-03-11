from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()

user_dependency = Annotated[User, Depends(get_current_user)]
db_dependency = Annotated[AsyncSession, Depends(get_db)]


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: user_dependency) -> User:
    return current_user

@router.patch('/me', response_model=UserResponse)
async def update_users_me(user_update: UserUpdate, current_user: user_dependency, db: db_dependency) -> User:
    
    update_data = user_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
        
    await db.commit()
    await db.refresh(current_user)
    
    return current_user