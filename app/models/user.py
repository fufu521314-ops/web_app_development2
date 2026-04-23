from datetime import datetime
from app.models import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    records = db.relationship('Record', backref='user', lazy=True)
    collections = db.relationship('Collection', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    @staticmethod
    def create(username, password_hash, email):
        """
        建立新使用者。
        :param username: 使用者名稱
        :param password_hash: 雜湊後的密碼
        :param email: 電子信箱
        :return: User 物件或 None
        """
        try:
            user = User(username=username, password_hash=password_hash, email=email)
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            print(f"建立使用者失敗: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有使用者"""
        try:
            return User.query.all()
        except Exception as e:
            print(f"取得所有使用者失敗: {e}")
            return []

    @staticmethod
    def get_by_id(user_id):
        """根據 ID 取得單一使用者"""
        try:
            return User.query.get(user_id)
        except Exception as e:
            print(f"取得使用者失敗 (ID: {user_id}): {e}")
            return None

    @staticmethod
    def get_by_username(username):
        """根據使用者名稱取得使用者"""
        try:
            return User.query.filter_by(username=username).first()
        except Exception as e:
            print(f"取得使用者失敗 (Username: {username}): {e}")
            return None

    def update(self, username=None, email=None, password_hash=None):
        """更新使用者資訊"""
        try:
            if username: self.username = username
            if email: self.email = email
            if password_hash: self.password_hash = password_hash
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"更新使用者失敗: {e}")
            return False

    def delete(self):
        """刪除使用者"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"刪除使用者失敗: {e}")
            return False
