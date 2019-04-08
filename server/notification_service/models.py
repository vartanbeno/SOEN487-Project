from flask_sqlalchemy import SQLAlchemy
import main

db = SQLAlchemy(main.app)


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}

class NotificationType(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    type = db.Column(db.Text(), nullable= False)

    def __repr__(self):
        return "<Type {}>".format(self.type)
