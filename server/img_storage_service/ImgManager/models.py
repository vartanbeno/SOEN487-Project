from ImgManager import db, login_manager
from flask_login import UserMixin


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns if c.name is not "password"}


@login_manager.user_loader
def load_user(user_id):
    return Client.query.get(int(user_id))


class Client(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), unique=True, nullable=False)

    def __repr__(self):
        return "<Person {}: {}>".format(self.id, self.name)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('Client.id'), nullable=False)

    def __repr__(self):
        return "<Album {}: {}, {}>".format(self.id, self.name, self.client_id)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    path = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return "<Album {}: {}, {}>".format(self.id, self.album_id, self.path)
