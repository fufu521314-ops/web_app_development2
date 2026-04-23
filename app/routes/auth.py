from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登入頁面與處理登入邏輯。
    GET: 渲染登入表單。
    POST: 驗證帳號密碼，成功後重導向至首頁。
    """
    pass

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    註冊頁面與處理註冊邏輯。
    GET: 渲染註冊表單。
    POST: 建立新使用者，成功後重導向至登入頁。
    """
    pass

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    處理登出邏輯。
    清除 Session 並重導向至首頁。
    """
    pass
