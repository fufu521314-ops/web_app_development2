from datetime import datetime
from app.models import db

class Novel(db.Model):
    __tablename__ = 'novels'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    cover_image = db.Column(db.String(200))
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    chapters = db.relationship('Chapter', backref='novel', lazy=True, cascade="all, delete-orphan")
    records = db.relationship('Record', backref='novel', lazy=True)
    collections = db.relationship('Collection', backref='novel', lazy=True)

    def __repr__(self):
        return f'<Novel {self.title}>'

    @staticmethod
    def create(title, author, description=None, category=None, cover_image=None):
        """建立新小說"""
        try:
            novel = Novel(title=title, author=author, description=description, 
                          category=category, cover_image=cover_image)
            db.session.add(novel)
            db.session.commit()
            return novel
        except Exception as e:
            db.session.rollback()
            print(f"建立小說失敗: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有小說"""
        try:
            return Novel.query.all()
        except Exception as e:
            print(f"取得所有小說失敗: {e}")
            return []

    @staticmethod
    def get_by_id(novel_id):
        """根據 ID 取得單一小說"""
        try:
            return Novel.query.get(novel_id)
        except Exception as e:
            print(f"取得小說失敗 (ID: {novel_id}): {e}")
            return None

    def update(self, title=None, author=None, description=None, category=None, cover_image=None, views=None):
        """更新小說資訊"""
        try:
            if title: self.title = title
            if author: self.author = author
            if description: self.description = description
            if category: self.category = category
            if cover_image: self.cover_image = cover_image
            if views is not None: self.views = views
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"更新小說失敗: {e}")
            return False

    def delete(self):
        """刪除小說"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"刪除小說失敗: {e}")
            return False

class Chapter(db.Model):
    __tablename__ = 'chapters'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    chapter_num = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Chapter {self.chapter_num}: {self.title}>'

    @staticmethod
    def create(novel_id, title, content, chapter_num):
        """建立新章節"""
        try:
            chapter = Chapter(novel_id=novel_id, title=title, content=content, chapter_num=chapter_num)
            db.session.add(chapter)
            db.session.commit()
            return chapter
        except Exception as e:
            db.session.rollback()
            print(f"建立章節失敗: {e}")
            return None

    @staticmethod
    def get_by_novel_id(novel_id):
        """取得特定小說的所有章節"""
        try:
            return Chapter.query.filter_by(novel_id=novel_id).order_by(Chapter.chapter_num).all()
        except Exception as e:
            print(f"取得章節失敗 (Novel ID: {novel_id}): {e}")
            return []

    @staticmethod
    def get_by_id(chapter_id):
        """根據 ID 取得單一章節"""
        try:
            return Chapter.query.get(chapter_id)
        except Exception as e:
            print(f"取得章節失敗 (ID: {chapter_id}): {e}")
            return None

    def update(self, title=None, content=None, chapter_num=None):
        """更新章節資訊"""
        try:
            if title: self.title = title
            if content: self.content = content
            if chapter_num is not None: self.chapter_num = chapter_num
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"更新章節失敗: {e}")
            return False

    def delete(self):
        """刪除章節"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"刪除章節失敗: {e}")
            return False
