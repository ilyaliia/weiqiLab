from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth import security
from core.dependencies import get_current_user
from database import get_session
from models.friends import Friends
from models.users import User
from schemas.users.base import UserBaseSchema
from schemas.users.update import UserUpdateSchema

router = APIRouter()


@router.get(
    "/users/{username}",
    response_model=UserBaseSchema,
    summary="Get user profile by username",
    description="Returns public user profile by username",
    tags=["Users 👤"]
)
async def get_user_by_name(
        username: str,
        session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, detail="User not found")
    return user


@router.get(
    "/users/me",
    summary="Get current user profile",
    description="Returns the profile of the authenticated user based on JWT token",
    tags=["Users 👤"]
)
async def get_profile(
        current_user=Depends(security.access_token_required),
        session: AsyncSession = Depends(get_session)
):
    user_id_str = current_user.sub  # user_id from token
    user_id = int(user_id_str)

    # search user by id
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one()  # user obj

    return {
        "user_id": user.id,
        "username": user.username,
        "email": user.email
    }


@router.patch(
    "/users/me",
    # response_model=UserBaseSchema,
    summary="Update current user profile",
    description="Update bio, avatar, country, language.",
    tags=["Users 👤"])
async def update_profile(
        update_data: UserUpdateSchema,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    if update_data.avatar_url is not None:
        current_user.avatar_url = update_data.avatar_url
    if update_data.bio is not None:
        current_user.bio = update_data.bio
    if update_data.country is not None:
        current_user.country = update_data.country
    if update_data.language is not None:
        current_user.language = update_data.language

    await session.commit()
    return {"updated": True}


@router.get(
    "/users/me/friends",
    summary="Get all my friends",
    description="Get list of friends for current user",
    tags=["Users 👤"]
)
async def get_my_friends(
        current_user=Depends(security.access_token_required),
        session: AsyncSession = Depends(get_session)
):
    user_id = int(current_user.sub)
    result = await session.execute(
        select(Friends).where(
            or_(
                Friends.sender_id == user_id,
                Friends.receiver_id == user_id
            ),
            Friends.status == "accepted"
        )
    )

    friend_relations = result.scalars().all()

    if not friend_relations:
        return []

    friend_ids = []
    for relation in friend_relations:
        if relation.sender_id == user_id:
            friend_ids.append(relation.receiver_id)
        else:
            friend_ids.append(relation.sender_id)

    friends_result = await session.execute(
        select(User).where(User.id.in_(friend_ids))
    )

    return friends_result.scalars().all()


@router.get(
    "/users/me/friends/requests",
    summary="Get friend requests",
    description="Get list of friend requests to current user",
    tags=["Users 👤"]
)
async def get_my_friends(
        current_user=Depends(security.access_token_required),
        session: AsyncSession = Depends(get_session)
):
    user_id = int(current_user.sub)
    result = await session.execute(
        select(Friends).where(
            or_(
                Friends.sender_id == user_id,
                Friends.receiver_id == user_id
            ),
            Friends.status == "pending"
        )
    )

    friend_relations = result.scalars().all()

    if not friend_relations:
        return []

    friend_ids = []
    for relation in friend_relations:
        if relation.sender_id == user_id:
            friend_ids.append(relation.receiver_id)
        else:
            friend_ids.append(relation.sender_id)

    friends_result = await session.execute(
        select(User).where(User.id.in_(friend_ids))
    )

    return friends_result.scalars().all()


@router.post(
    "/users/me/friends/{user_id}",
    summary="Send friend request",
    description="Send friend request from current user by id",
    tags=["Users 👤"]
)
async def add_friend(
        user_id: int,
        current_user=Depends(security.access_token_required),
        session: AsyncSession = Depends(get_session),
):
    my_id = int(current_user.sub)
    if my_id == user_id:
        return {"error": "Cannot add yourself"}

    user = await session.get(User, user_id)
    if not user:
        return {"error": "User not found"}

    # is exist
    existing = await session.execute(
        select(Friends).where(
            Friends.sender_id == my_id,
            Friends.receiver_id == user_id
        )
    )
    if existing.scalar_one_or_none():
        return {"error": "Friend request already exists"}

    # Создаем новую заявку
    new_friend = Friends(
        sender_id=my_id,
        receiver_id=user_id,
        status="pending"
    )
    session.add(new_friend)
    await session.commit()
    return {"message": "Success send friend request"}


@router.patch(
    "/users/me/friends/{user_id}",
    summary="Respond to friend request",
    description="Accept or decline friend request",
    tags=["Users 👤"]
)
async def respond_to_friend_request(
    user_id: int,
    action: str,
    current_user=Depends(security.access_token_required),
    session: AsyncSession = Depends(get_session)
):
    my_id = int(current_user.sub)

    # search respond
    result = await session.execute(
        select(Friends).where(
            Friends.sender_id == user_id,
            Friends.receiver_id == my_id,
            Friends.status == "pending"
        )
    )
    friend_request = result.scalar_one_or_none()

    if not friend_request:
        return {"error": "Friend request not found"}

    if action == "accept":
        friend_request.status = "accepted"
    elif action == "decline":
        friend_request.status = "declined"
    else:
        return {"error": "Action must be 'accept' or 'decline'"}

    await session.commit()
    return {"message": f"Friend request {action}ed"}