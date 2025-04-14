
from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
import auth_routes
import role_routes
from config import Settings
from functools import wraps
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, database
from fastapi import Depends

app = FastAPI()


@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth_routes.auth_router)
app.include_router(role_routes.role_router)

def require_role(role: models.RoleEnum):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            db = kwargs.get('db')
            Authorize = kwargs.get('Authorize')
            
            Authorize.jwt_required()
            current_user_email = Authorize.get_jwt_subject()
            user = db.query(models.User).filter(
                models.User.email == current_user_email
            ).first()
            
            if not user or user.role.name != role:
                raise HTTPException(
                    status_code=403,
                    detail=f"Role {role} required"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Usage:
# @router.get("/admin-only")
@require_role(models.RoleEnum.ADMIN)
async def admin_route(db: Session = Depends(database.get_db),
                     Authorize: AuthJWT = Depends()):
    return {"message": "Admin access granted"}

# In your initialization script
roles = [
    {"name": models.RoleEnum.ADMIN, "description": "Administrator"},
    {"name": models.RoleEnum.USER, "description": "Regular user"},
    {"name": models.RoleEnum.STAFF, "description": "Staff member"},
]

# for role_data in roles:
#     role = models.Role(**role_data)
#     db.add(role)
# db.commit()

# # When creating a user
# user = User(
#     username="admin",
#     email="admin@example.com",
#     password=hashed_password,
#     role_id=admin_role.id
# )
