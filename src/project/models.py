from project import db


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    correo = db.Column(db.String, nullable=False)
    direccion = db.Column(db.String, nullable=True)


class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    razon_social = db.Column(db.String, nullable=False)
