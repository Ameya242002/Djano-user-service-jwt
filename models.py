from sqlalchemy import Column, Integer, String, Boolean, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import enum

# Define Role Enum
class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"
    STAFF = "staff"

# Create Role Model
class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(Enum(RoleEnum), unique=True, nullable=False)
    description = Column(String(200))

    # Relationship with users
    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role {self.name}>"

# Modify User Model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    
    # Add role relationship
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role", back_populates="users")
    
    # Add tasks relationship
    # tasks = relationship("Task", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"