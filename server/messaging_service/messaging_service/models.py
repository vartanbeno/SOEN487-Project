from datetime import datetime

from messaging_service import db


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_id = db.Column(db.Integer)
    participant_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    messages = db.relationship('Message', backref='conversation')

    def json(self):
        return {
            'id': self.id,
            'creator_id': self.creator_id,
            'participant_id': self.participant_id,
            'created_at': self.created_at,
            'messages': [message.json() for message in self.messages]
        }


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    sender_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'created_at': self.created_at,
            'text': self.text
        }
