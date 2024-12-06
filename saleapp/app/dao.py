from models import Category, Products, User
import hashlib
from __init__ import app, db
import cloudinary.uploader


def load_categories():
    return Category.query.order_by('id').all()


def load_products(cate_id=None, kw=None, page=1):
    query = Products.query
    if kw:
        query = query.filter(Products.name.contains(kw))
    if cate_id:
        query = query.filter(Products.category_id == cate_id)

    page_size =app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    query = query.slice(start, start + page_size)

    return query.all()


def count_products():
    return Products.query.count()


def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username), User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def add_user(name, username, password,
             avatar=None):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password)
    if avatar:
        res = cloudinary.uploader.upload(avatar)
        res.get('secure.url')

    db.session.add(u)
    db.session.commit()
