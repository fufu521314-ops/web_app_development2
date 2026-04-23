from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登入頁面與處理登入邏輯。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.get_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('登入成功！', 'success')
            return redirect(url_for('main.index'))
        
        flash('帳號或密碼錯誤。', 'danger')
        
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    註冊頁面與處理註冊邏輯。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # 簡易驗證
        if not username or not email or not password:
            flash('請填寫所有必填欄位。', 'warning')
            return render_template('auth/register.html')
            
        if User.get_by_username(username):
            flash('此帳號已存在。', 'danger')
            return render_template('auth/register.html')

        hashed_password = generate_password_hash(password)
        new_user = User.create(username=username, email=email, password_hash=hashed_password)
        
        if new_user:
            flash('註冊成功，請登入。', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('註冊失敗，請稍後再試。', 'danger')
            
    return render_template('auth/register.html')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    處理登出邏輯。
    """
    session.clear()
    flash('您已成功登出。', 'info')
    return redirect(url_for('main.index'))
