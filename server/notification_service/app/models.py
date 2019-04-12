from app import db


class NotificationType(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    type = db.Column(db.Text(), nullable= False)

    def __repr__(self):
        return "<Type {}>".format(self.type)

    def json(self):
        return {
            'id': self.id,
            'type': self.type
        }
