"""
Copyright © 2024 [tranandeveloper@gmail.com]
All Rights Reserved.

Licensed under the MIT License. You may obtain a copy of the License at:
    https://opensource.org/licenses/MIT

Author: TranAn
"""

import uuid

from sqlalchemy import JSON, TEXT, TIMESTAMP, Boolean, Column, Integer, String
from sqlalchemy.sql import func

from databases.postgresql import BaseModel
from providers.postgresql.orm_client import DeclarativeBaseQ


class User(
    BaseModel,
    DeclarativeBaseQ
):
    """
    The User class represents the 'users' table in the database.

    Fields in this table include:
    - id: Primary key, a unique identifier for each user.
    - username: User's login name (unique, not duplicated).
    - email: User's email address (unique, not duplicated).
    - password_hash: User's hashed password (using bcrypt/argon2).
    - public_key: User's public key.
    - private_key_encrypted: User's encrypted private key.
    - recovery_phrase_encrypted: User's encrypted recovery phrase.
    - blockchain_address: User's unique blockchain wallet address.
    - block_hash_last: The hash of the last block related to the user.
    - user_metadata: Additional metadata about the user (JSON format).
    - failed_login_attempts: The number of failed login attempts.
    - is_verified: Whether the user has verified their account.
    - account_status: Status of the account (active, suspended, deleted).
    - is_active: Whether the account is currently active.
    - is_deleted: Flag indicating if the account is deleted.
    - created_at: Account creation timestamp.
    - updated_at: Last update timestamp.
    """

    __tablename__ = "users"

    # Primary Key
    id = Column(
        String(36), default=lambda: str(uuid.uuid4()), primary_key=True, index=True
    )

    # User Info
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(
        String(255), nullable=False
    )  # Ensure proper length for hashed password
    public_key = Column(TEXT, unique=True, nullable=True)
    private_key_encrypted = Column(TEXT, nullable=True)
    recovery_phrase_encrypted = Column(TEXT, nullable=True)
    blockchain_address = Column(
        String(100), unique=True, nullable=True
    )  # Blockchain address

    # Metadata & State
    block_hash_last = Column(
        String(64), nullable=True
    )  # Hash of last block related to the user
    user_metadata = Column(JSON, nullable=True)  # Store any extra metadata

    # Authentication & Status
    failed_login_attempts = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False)  # Account verification status
    is_active = Column(Boolean, default=True)  # Account active status
    is_deleted = Column(Boolean, default=False)  # Soft delete flag

    # Timestamps
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email}, is_activate={self.is_active})>"
