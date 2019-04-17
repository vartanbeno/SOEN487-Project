from flask_sqlalchemy import SQLAlchemy
from app import app
from datetime import datetime
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.Text(), nullable=False, unique=True)
#     createdConvo = db.relationship("Conversation", backref="creator", lazy="dynamic", foreign_keys="Conversation.creator_id")
#     participantConvo = db.relationship("Conversation", backref="participant", lazy="dynamic" ,foreign_keys="Conversation.participant_id")
#     messages_sent = db.relationship("Message")
    # def __repr__(self):
    #     return "<User {}: {}>".format(self.id, self.username)


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator = db.Column(db.Integer, nullable=False)
    participant = db.Column(db.Integer, nullable=False)
    messages = db.relationship("Message", backref="messages")


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    sender = db.Column(db.Integer, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    text = db.Column(db.Text(), nullable=False)
