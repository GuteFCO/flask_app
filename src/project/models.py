from project import db


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    correo = db.Column(db.String, nullable=False)
