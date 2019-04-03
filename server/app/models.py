import re
from random import choice
from string import ascii_letters, digits

from app import db
from app.exceptions.ModelValidationException import ModelValidationException

email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    verification = db.relationship('Verification', uselist=False, backref='user', lazy=True)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.email}, {self.username})'

    def validate(self):
        """
        Validate user object. An exception is thrown if one of the following conditions isn't met:
            - user must have a valid email
            - user's username must be between 4-30 characters
        :return: None
        """
        if not email_regex.match(self.email):
            raise ModelValidationException("A user must provide a valid email address.")

        if self.username is None or not 4 <= len(self.username) <= 30:
            raise ModelValidationException("A user's username must be between 4 and 30 characters.")

    def is_verified(self):
        return self.verification is None

    def json(self):
        """
        Using custom methods instead of row2dict because we don't want to return a user's password to the client (even
        thought it's hashed). We can decide what to return to the client ourselves instead of returning all attributes.
        :return: dictionary containing relevant user attributes
        """
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username
        }


class Verification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.key})'

    def generate_random_key(self):
        """
        Assigns a random 300-character long key to the entity which will be used to verify the newly created account.
        You can verify by making a GET/POST request to /api/auth/verify?key=[key]
        :return: None
        """
        self.key = ''.join(choice(ascii_letters + digits) for i in range(300))

    def json(self):
        return {
            'id': self.id,
            'key': self.key,
            'user': self.user.json()
        }
