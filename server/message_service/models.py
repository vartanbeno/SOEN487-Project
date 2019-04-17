from flask_sqlalchemy import SQLAlchemy
from app import app
from datetime import datetime
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_id = db.Column(db.Integer)
    participant_id = db.Column(db.Integer)
    messages = db.relationship("Message", backref="messages")


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    sender_id = db.Column(db.Integer)
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text(), nullable=False)
