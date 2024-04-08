from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


class sections(db.Model):
    section_id = db.Column(db.Integer,primary_key=True)
    section_name=db.Column(db.String(10000))
    section_img_link=db.Column(db.String(10000))
    
    
class product(db.Model):
    product_id = db.Column(db.Integer,primary_key=True)
    product_name=db.Column(db.String(10000))
    product_price=db.Column(db.Integer)
    product_mdate=db.Column(db.String(10000))
    img_link=db.Column(db.String(10000))
    procat_id=db.Column(db.Integer,db.ForeignKey(sections.section_id))


class tester(db.Model):
    t_name = db.Column(db.String(10000),primary_key=True)
    t_quantity = db.Column(db.Integer)
    t_price = db.Column(db.Integer)
    t_total = db.Column(db.Integer)

    

