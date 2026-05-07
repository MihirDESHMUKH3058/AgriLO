from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

import models
from schemas import auth as schemas
from dependencies import get_current_active_user
from datetime import datetime

router = APIRouter()

@router.put("/me", response_model=schemas.UserResponse)
async def update_user_me(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Update current user's profile and settings.
    """
    # Create a dict of updates, excluding None values
    update_data = user_update.dict(exclude_unset=True)
    
    # Handle specific validations if necessary (e.g. email uniqueness if email is updatable)
    # For now, we are not allowing email updates in the schema or excluding it here if it was present
    
    # Update user model
    for key, value in update_data.items():
        setattr(current_user, key, value)
        
    current_user.updated_at = datetime.utcnow()
    
    await current_user.save()
    
    return current_user
