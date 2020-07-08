from project import db, bcrypt


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    correo = db.Column(db.String, nullable=False)
    direccion = db.Column(db.String, nullable=True)

    def __init__(self, **kwargs):
        super(Usuario, self).__init__(**kwargs)
        self.password = self.generate_password_hash(**kwargs)

    def generate_password_hash(self, **kwargs):
        if 'password' in kwargs:
            return bcrypt.generate_password_hash(kwargs['password']).decode()

        return None


class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    razon_social = db.Column(db.String, nullable=False)
