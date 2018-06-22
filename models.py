from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from ballista import db
# TODO: class Round: id, name, caliber
# TODO: Rifle-Round Muzzle Velocity
# TODO: class Target


class Caliber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caliber_name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<CALIBER ID {self.id}: {self.caliber_name}>"


class Rifle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    barrel_length = db.Column(db.Float)
    created_dt = db.Column(db.DateTime, default=datetime.now())
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    caliber_id = db.Column(db.Integer, db.ForeignKey('caliber.id'), nullable=False)

    caliber = db.relationship('Caliber')

    @staticmethod
    def get_by_rifle_name(rifle_name):
        return Rifle.query.filter_by(name=rifle_name).first()

    def __repr__(self):
        return f'<RIFLE ID {self.id}: {self.name}>'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    rifles = db.relationship('Rifle', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String)
    selected_rifle = db.Column(db.Integer, nullable=True)
    selected_round = db.Column(db.Integer, nullable=True)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return f"<USER ID:{self.id}: {self.username}>"
