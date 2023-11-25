from . import db 
from flask_login import UserMixin
# бд здесь чисто для вида, потом на норм заменить
from sqlalchemy.sql import func


"""
Тут будут классы пользователей, пока тут лишь шаблон есть
"""


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))