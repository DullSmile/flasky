"""检查用户权限的自定义修饰器"""
from functools import wraps
from app.models import Permission
from flask import abort
from flask_login import current_user


def permission_required(permission):
    def deorator(f):
        @wraps(f)
        def deorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return deorated_function

def admin_required(f):
    return permission_required(Permission.MODERATE_COMMENTS)(f)