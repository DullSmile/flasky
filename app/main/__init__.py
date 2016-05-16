# -*-coding:utf-8-*-
from app.models import Permission
from flask import Blueprint

main = Blueprint('main', __name__)

#把Permission类加入模板上下文
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


#导入views,errors模块能把路由和处理错误程序与蓝本关联起来.
#注意,这些模块在脚本末尾导入,是为了笔漫循环导入依赖,因为在views.py和errors.py中还要导入蓝本main
from . import views, errors