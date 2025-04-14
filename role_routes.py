from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database
from fastapi_jwt_auth import AuthJWT

role_router = APIRouter(prefix="/roles", tags=["roles"])

# Create role
@role_router.post("/", response_model=schemas.RoleOut)
async def create_role(
    role: schemas.RoleCreate,
    db: Session = Depends(database.get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    
    # Check if user is admin (you might want to implement this)
    db_role = models.Role(name=role.name, description=role.description)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

# Get all roles
@role_router.get("/", response_model=List[schemas.RoleOut])
async def get_roles(
    db: Session = Depends(database.get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    return db.query(models.Role).all()

# Assign role to user
@role_router.put("/users/{user_id}/role/{role_id}")
async def assign_role_to_user(
    user_id: int,
    role_id: int,
    db: Session = Depends(database.get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    user.role_id = role.id
    db.commit()
    db.refresh(user)
    return {"message": f"Role {role.name} assigned to user {user.username}"}