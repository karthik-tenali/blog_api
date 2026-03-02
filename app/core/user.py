# app/core/user.py
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.utils.hash import hash_password, verify_password


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_uid(db: AsyncSession, uid: uuid.UUID) -> User | None:
    result = await db.execute(select(User).where(User.uid == uid))
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    email: str,
    username: str,
    first_name: str,
    last_name: str,
    password: str,
) -> User:

    if await get_user_by_email(db, email):
        raise ValueError("Email already registered")

    result = await db.execute(select(User).where(User.username == username))
    if result.scalar_one_or_none():
        raise ValueError("Username already taken")

    user = User(
        email=email,
        username=username,
        first_name=first_name,
        last_name=last_name,
        hashed_password=hash_password(password),
    )

    db.add(user)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ValueError("User already exists")

    await db.refresh(user)
    return user


async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str,
) -> User | None:

    user = await get_user_by_email(db, email)

    if not user:
        return None

    if not user.is_active:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user