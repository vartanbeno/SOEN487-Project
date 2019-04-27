from app import db

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    senderID = db.Column(db.Integer, nullable=False)
    receiverID = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable= True)

    def __repr__(self):
        return "<Message sent by User ID {} to User ID {}>".format(self.senderID, self.receiverID)

    def json(self):
        return {
            'id': self.id,
            'senderID': self.senderID,
            'receiverID': self.receiverID,
            'message': self.message
        }
