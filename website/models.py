from website import db
from flask_login import UserMixin
from sqlalchemy.sql import  func
from sqlalchemy import Date

# Definice modelu Client
class Client(db.Model):
    # Definice sloupců tabulky
    id = db.Column(db.Integer, primary_key=True)
    jmeno = db.Column(db.String(1000))
    prijmeni = db.Column(db.String(1000))
    datum_narozeni = db.Column(Date)
    telefon = db.Column(db.String(100))
    email = db.Column(db.String(10000))
    ulice = db.Column(db.String(10000))
    cp = db.Column(db.String(100))
    mesto = db.Column(db.String(10000))
    psc = db.Column(db.String(7))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# Definice modelu User
class User(db.Model, UserMixin):
    # Definice sloupců tabulky
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    heslo = db.Column(db.String(150))
    jmeno = db.Column(db.String(150))
    prijmeni = db.Column(db.String(150))
    datum_narozeni = db.Column(Date)
    clients = db.relationship('Client')

# Definice modelu Pojisteni
class Pojisteni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazev = db.Column(db.String(200))
    castka = db.Column(db.Integer)
    predmet = db.Column(db.String(200))
    platnost_od = db.Column(Date)
    platnost_do = db.Column(Date)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    pojisteni = db.relationship('Client')
