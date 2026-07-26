from typing import List
from fastapi import Depends
from models.user import User
from dependencies.auth_dependency import get_current_active_user
from exceptions.custom import PermissionDeniedException

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise PermissionDeniedException(
                f"Role '{current_user.role}' is not authorized. Required one of: {self.allowed_roles}"
            )
        return current_user
