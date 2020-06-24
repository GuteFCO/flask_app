from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


class Config:
    # protocolo://usuario:password@host:puerto/basededatos
    SQLALCHEMY_DATABASE_URI = 'postgres://fgutierrez:optativo123@35.224.193.212:5432/fgutierrez'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


db = SQLAlchemy()
app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=True)


def usuario_a_dict(usuario):
    return {'id': usuario.id, 'nombre': usuario.nombre}


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

    db.session.add(usuario)
    db.session.commit()

    return usuario_a_dict(usuario), 200


@app.route('/users/<id>', methods=['PATCH'])
def patch(id):
    usuario = Usuario.query.get_or_404(id)
    datos = request.get_json()

    usuario.nombre = datos.get('nombre', usuario.nombre)
    usuario.password = datos.get('password', usuario.password)

    db.session.add(usuario)
    db.session.commit()

    return usuario_a_dict(usuario), 200


@app.route('/users/<id>', methods=['DELETE'])
def delete(id):
    usuario = Usuario.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    return '', 204
