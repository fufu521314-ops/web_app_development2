from datetime import datetime
from app.models import db

class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), nullable=False)
    last_chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Record User:{self.user_id} Novel:{self.novel_id}>'

    @staticmethod
    def create_or_update(user_id, novel_id, last_chapter_id):
        record = Record.query.filter_by(user_id=user_id, novel_id=novel_id).first()
        if record:
            record.last_chapter_id = last_chapter_id
        else:
            record = Record(user_id=user_id, novel_id=novel_id, last_chapter_id=last_chapter_id)
            db.session.add(record)
        db.session.commit()
        return record

    @staticmethod
    def get_by_user(user_id):
        return Record.query.filter_by(user_id=user_id).all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Collection(db.Model):
    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Collection User:{self.user_id} Novel:{self.novel_id}>'

    @staticmethod
    def add(user_id, novel_id):
        collection = Collection.query.filter_by(user_id=user_id, novel_id=novel_id).first()
        if not collection:
            collection = Collection(user_id=user_id, novel_id=novel_id)
            db.session.add(collection)
            db.session.commit()
        return collection

    @staticmethod
    def remove(user_id, novel_id):
        collection = Collection.query.filter_by(user_id=user_id, novel_id=novel_id).first()
        if collection:
            db.session.delete(collection)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_by_user(user_id):
        return Collection.query.filter_by(user_id=user_id).all()
