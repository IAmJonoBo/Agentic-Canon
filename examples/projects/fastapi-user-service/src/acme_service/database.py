"""In-memory database for demonstration purposes."""

from typing import Dict, Optional
from uuid import UUID

from acme_service.models import UserInDB


class UserDatabase:
    """Simple in-memory user database."""

    def __init__(self) -> None:
        """Initialize empty database."""
        self.users: Dict[UUID, UserInDB] = {}
        self.email_index: Dict[str, UUID] = {}

    def create(self, user: UserInDB) -> UserInDB:
        """Create a new user."""
        self.users[user.id] = user
        self.email_index[user.email] = user.id
        return user

    def get(self, user_id: UUID) -> Optional[UserInDB]:
        """Get user by ID."""
        return self.users.get(user_id)

    def get_by_email(self, email: str) -> Optional[UserInDB]:
        """Get user by email."""
        user_id = self.email_index.get(email)
        if user_id:
            return self.users.get(user_id)
        return None

    def update(self, user_id: UUID, user: UserInDB) -> Optional[UserInDB]:
        """Update an existing user."""
        if user_id in self.users:
            # Update email index if email changed
            old_email = self.users[user_id].email
            if old_email != user.email:
                del self.email_index[old_email]
                self.email_index[user.email] = user_id
            self.users[user_id] = user
            return user
        return None

    def delete(self, user_id: UUID) -> bool:
        """Delete a user."""
        if user_id in self.users:
            email = self.users[user_id].email
            del self.users[user_id]
            del self.email_index[email]
            return True
        return False

    def list_all(self) -> list[UserInDB]:
        """List all users."""
        return list(self.users.values())


# Global database instance
db = UserDatabase()
