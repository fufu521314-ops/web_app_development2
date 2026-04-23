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
        novel = Novel(title=title, author=author, description=description, 
                      category=category, cover_image=cover_image)
        db.session.add(novel)
        db.session.commit()
        return novel

    @staticmethod
    def get_all():
        return Novel.query.all()

    @staticmethod
    def get_by_id(novel_id):
        return Novel.query.get(novel_id)

    def update(self, title=None, author=None, description=None, category=None, cover_image=None, views=None):
        if title: self.title = title
        if author: self.author = author
        if description: self.description = description
        if category: self.category = category
        if cover_image: self.cover_image = cover_image
        if views is not None: self.views = views
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

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
        chapter = Chapter(novel_id=novel_id, title=title, content=content, chapter_num=chapter_num)
        db.session.add(chapter)
        db.session.commit()
        return chapter

    @staticmethod
    def get_by_novel_id(novel_id):
        return Chapter.query.filter_by(novel_id=novel_id).order_by(Chapter.chapter_num).all()

    @staticmethod
    def get_by_id(chapter_id):
        return Chapter.query.get(chapter_id)

    def update(self, title=None, content=None, chapter_num=None):
        if title: self.title = title
        if content: self.content = content
        if chapter_num is not None: self.chapter_num = chapter_num
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
