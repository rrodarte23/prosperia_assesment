from typing import List

from fastapi import APIRouter, HTTPException

from ..mongo_db_utils import (
    create_user,
    read_all_users,
    read_user_by_id,
    update_user,
    delete_user
)
from ..models.user import User, UserRequest

router = APIRouter()


@router.post('/user', response_model=User)
def add_new_user(user: UserRequest):
    """
    Create a new user.
    """
    user_id = create_user(user)
    return {**user.dict(), "id": user_id}


@router.get("/users/", response_model=List[User])
def get_all_users() -> List[User]:
    """
    Retrieve all users.
    """
    return read_all_users()


@router.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: int) -> User:
    """
    Retrieve a user by ID.
    """
    user = read_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=User)
def update_user_by_id(user_id: int, new_data: UserRequest) -> User:
    """
    Update a user by ID.
    """
    updated_count = update_user(user_id, new_data)
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return get_user_by_id(user_id)


@router.delete("/users/{user_id}")
def delete_user_by_id(user_id: int):
    """
    Delete a user by ID.
    """
    deleted_count = delete_user(user_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
