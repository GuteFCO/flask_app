from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


class Config:
    # protocolo://usuario:password@host:puerto/basededatos
    SQLALCHEMY_DATABASE_URI = 'postgres://fgutierrez:optativo123@35.224.193.212:5432/fgutierrez'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


db = SQLAlchemy()
migrate = Migrate()
app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    correo = db.Column(db.String, nullable=False)


def usuario_a_dict(usuario):
    return {'id': usuario.id, 'nombre': usuario.nombre, 'correo': usuario.correo}


@app.route('/')
def index():
    return '<h1>Hola</h1>'


@app.route('/register', methods=['POST'])
@app.route('/users', methods=['POST'])
def register():
    datos = request.get_json()

    usuario = Usuario(**datos)

    db.session.add(usuario)
    db.session.commit()

    return usuario_a_dict(usuario), 201


@app.route('/users', methods=['GET'])
def list():
    usuarios = Usuario.query.all()

    respuesta = []

    for usuario in usuarios:
        respuesta.append(usuario_a_dict(usuario))

    return jsonify(respuesta), 200


@app.route('/users/<id>', methods=['GET'])
def view(id):
    usuario = Usuario.query.get_or_404(id)

    return usuario_a_dict(usuario), 200


@app.route('/users/<id>', methods=['PUT'])
def update(id):
    usuario = Usuario.query.get_or_404(id)
    datos = request.get_json()

    usuario.nombre = datos['nombre']
    usuario.password = datos['password']
    usuario.correo = datos['correo']

    db.session.add(usuario)
    db.session.commit()

    return usuario_a_dict(usuario), 200


@app.route('/users/<id>', methods=['PATCH'])
def patch(id):
    usuario = Usuario.query.get_or_404(id)
    datos = request.get_json()

    usuario.nombre = datos.get('nombre', usuario.nombre)
    usuario.password = datos.get('password', usuario.password)
    usuario.correo = datos.get('correo', usuario.correo)

    db.session.add(usuario)
    db.session.commit()

    return usuario_a_dict(usuario), 200


@app.route('/users/<id>', methods=['DELETE'])
def delete(id):
    usuario = Usuario.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    return '', 204
