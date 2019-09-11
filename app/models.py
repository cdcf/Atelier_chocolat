from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(32), index=True)
    second_name = db.Column(db.String(32), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(256))
    password_hash = db.Column(db.String(128))
    productions = db.relationship('Production', backref='author', lazy='dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_productions(self):
        followed = Production.query.join(
            followers, (followers.c.followed_id == Production.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Production.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Production.id.desc())

    def my_productions(self):
        own = Production.query.filter_by(user_id=self.id)
        return own.order_by(Production.id.desc())

    def get_reset_password_token(self, expires_in=120):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Production(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)
    name = db.Column(db.String(64), index=True)
    comment = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Production {}>'.format(self.name)


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4), index=True, unique=True)
    description = db.Column(db.String(64))
    default_curr = db.Column(db.Boolean())

    def __repr__(self):
        return '<Currency {}>'.format(self.name)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4), index=True, unique=True)
    origin = db.Column(db.String(32), index=True)
    organic = db.Column(db.Boolean())
    fair_trade = db.Column(db.Boolean())
    crop = db.Column(db.Integer)
    comment = db.Column(db.Text())
    colour = db.Column(db.String(16))
    product_family_id = db.Column(db.Integer, db.ForeignKey('product_family.id'))

    def __repr__(self):
        return '<Product>'.format(self.name)


class ProductFamily(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    icon = db.Column(db.String(32))
    product = db.relationship('Product', backref='product_product', lazy='dynamic')

    def __repr__(self):
        return '<ProductFamily<>'.format(self.name)


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    address = db.Column(db.Text())
    email = db.Column(db.String(120))
    telephone = db.Column(db.String(24))
    website = db.Column(db.String(56))
