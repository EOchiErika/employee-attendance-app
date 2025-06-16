from __main__ import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'trabajador'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    dni = db.Column(db.String(20))
    legajo = db.Column(db.String(20))
    correo = db.Column(db.String(100))
    horas = db.Column(db.Integer)
    funcion = db.Column(db.String(2))
    registro = db.relationship('Registro', backref='trabajador', cascade="all, delete-orphan")


class Registro(db.Model):
    __tablename__ = 'registrohorario'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    horaentrada = db.Column(db.Time)
    horasalida = db.Column(db.Time)
    dependencia = db.Column(db.String(4))
    idtrabajador = db.Column(db.Integer, db.ForeignKey('trabajador.id'))