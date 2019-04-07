from flask_sqlalchemy import SQLAlchemy
import main

db = SQLAlchemy(main.app)


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    password = db.Column(db.Text(), nullable= False)
    email = db.Column(db.Text(), nullable = False)
    notifications = db.Column(db.BOOLEAN, nullable= False)
    notificationType = db.Column(db.Text(), db.ForeignKey('notification_type.type'),nullable= False)

    def __repr__(self):
        return "<Person {}: {}, email: {}>".format(self.id, self.name, self.email)

class Admin(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)

    def __repr__(self):
        return "<Admin {}>".format(self.id)

class NotificationType(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    type = db.Column(db.Text(), nullable= False)

    def __repr__(self):
        return "<Type {}>".format(self.type)
