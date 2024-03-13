from datetime import datetime
from typing import Dict, Any, Union

from pymongo import MongoClient
from bson.objectid import ObjectId

from .models.user import User, UserRequest

client = MongoClient("172.18.0.2", port=27017)
db = client["prosperia"]
users_collection = db["users"]
sequence_collection = db["sequences"]


def get_next_sequence_value(sequence_name):
    """
    Get the next sequence value for the given sequence name.
    If the sequence does not exist, create it and initialize its value to 1.
    """
    sequence_doc = sequence_collection.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"value": 1}},
        upsert=True,
        return_document=True
    )
    return int(sequence_doc["value"])


def generate_user_id():
    return get_next_sequence_value("user_id_sequence")


def create_user(user: UserRequest) -> int:
    """
    Create a new user document.

    :param user: The user data to create the document.
    :type user: User
    :return: The ObjectId of the newly created user document.
    :rtype: ObjectId
    """
    user_data = user.dict()
    new_user_id = generate_user_id()
    if isinstance(new_user_id, ObjectId):
        new_user_id = int(str(new_user_id), 16)
    user_data["id"] = new_user_id
    user_data["creation_time"] = datetime.now()
    users_collection.insert_one(user_data)
    return new_user_id


def read_all_users() -> list[User]:
    """
    Retrieve all user documents.

    :return: List of user documents.
    :rtype: list[User]
    """
    users_data = list(users_collection.find())
    return [User(
        id=str(user_data['id']),
        name=user_data['name'],
        last_name=user_data['last_name'],
        phone_number=user_data['phone_number'],
        age=user_data['age'],
        creation_time=user_data['creation_time']
        ) for user_data in users_data]


def read_user_by_id(user_id: int) -> Union[User, None]:
    """
    Retrieve a user document by ID.

    :param user_id: The ObjectId of the user document to retrieve.
    :type user_id: int
    :return: The user document, or None if not found.
    :rtype: Union[User, None]
    """
    user_data = users_collection.find_one({"id": user_id})
    if user_data:
        return User(**user_data)
    return None


def update_user(user_id: int, new_data: UserRequest) -> int:
    """
    Update a user document by ID.

    :param user_id: The ObjectId of the user document to update.
    :type user_id: int
    :param new_data: New data to update the user document with.
    :type new_data: dict
    :return: The number of documents updated (0 or 1).
    :rtype: int
    """
    result = users_collection.update_one({"id": user_id}, {"$set": new_data.dict()})
    return result.modified_count


def delete_user(user_id: int) -> int:
    """
    Delete a user document by ID.

    :param user_id: The ObjectId of the user document to delete.
    :type user_id: int
    :return: The number of documents deleted (0 or 1).
    :rtype: int
    """
    result = users_collection.delete_one({"id": user_id})
    return result.deleted_count
