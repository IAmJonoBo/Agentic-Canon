"""FastAPI User Service - Main application."""

from datetime import datetime
from typing import List
from uuid import UUID

from acme_service.database import db
from acme_service.models import User, UserCreate, UserInDB, UserUpdate
from acme_service.security import get_password_hash
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="FastAPI User Service",
    description="A production-ready FastAPI microservice for user management",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["health"])
async def root() -> dict:
    """Root endpoint - health check."""
    return {
        "status": "healthy",
        "service": "FastAPI User Service",
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/health", tags=["health"])
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/ready", tags=["health"])
async def ready() -> dict:
    """Readiness check endpoint."""
    return {"status": "ready"}


@app.post(
    "/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=["users"]
)
async def create_user(user_data: UserCreate) -> User:
    """Create a new user."""
    # Check if user with email already exists
    existing_user = db.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    # Create user in database
    hashed_password = get_password_hash(user_data.password)
    user_in_db = UserInDB(
        **user_data.model_dump(exclude={"password"}),
        hashed_password=hashed_password,
    )
    created_user = db.create(user_in_db)

    # Return user without password
    return User(**created_user.model_dump(exclude={"hashed_password"}))


@app.get("/users", response_model=List[User], tags=["users"])
async def list_users() -> List[User]:
    """List all users."""
    users = db.list_all()
    return [User(**user.model_dump(exclude={"hashed_password"})) for user in users]


@app.get("/users/{user_id}", response_model=User, tags=["users"])
async def get_user(user_id: UUID) -> User:
    """Get a user by ID."""
    user = db.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return User(**user.model_dump(exclude={"hashed_password"}))


@app.put("/users/{user_id}", response_model=User, tags=["users"])
async def update_user(user_id: UUID, user_data: UserUpdate) -> User:
    """Update a user."""
    existing_user = db.get(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Check if email is being changed and already exists
    if user_data.email and user_data.email != existing_user.email:
        email_user = db.get_by_email(user_data.email)
        if email_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

    # Update user fields
    update_data = user_data.model_dump(exclude_unset=True)
    if "password" in update_data:
        hashed_password = get_password_hash(update_data.pop("password"))
        update_data["hashed_password"] = hashed_password

    update_data["updated_at"] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(existing_user, field, value)

    updated_user = db.update(user_id, existing_user)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user",
        )

    return User(**updated_user.model_dump(exclude={"hashed_password"}))


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_user(user_id: UUID) -> None:
    """Delete a user."""
    success = db.delete(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
