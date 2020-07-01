import datetime
import jwt
from flask import request, jsonify, Blueprint
from project import db
from project.models import Usuario


blueprint = Blueprint('usuarios', __name__)


def usuario_a_dict(usuario):
    return {
        'id': usuario.id,
        'nombre': usuario.nombre,
        'correo': usuario.correo}


def check_token():
    authorization = request.headers.get('Authorization')

    if authorization is None:
        return False

    partes = authorization.split(' ')
    if len(partes) != 2:
        return False

    if partes[0] != 'Bearer':
        return False

    token = partes[1]

    try:
        return jwt.decode(token, '123456')
    except:
        return False


def autenticar(f):
    def wrapper():
        if check_token() is False:
            return 'Unauthorized', 401
        return f()
    return wrapper


@blueprint.route('/register', methods=['POST'])
@blueprint.route('/users', methods=['POST'])
def register():
    datos = request.get_json()

    usuario = Usuario(**datos)

    db.session.add(usuario)
    db.session.commit()

    return usuario_a_dict(usuario), 201


@blueprint.route('/users', methods=['GET'])
@autenticar
def list():
    usuarios = Usuario.query.all()

    respuesta = []

    for usuario in usuarios:
        respuesta.append(usuario_a_dict(usuario))

    return jsonify(respuesta), 200


@blueprint.route('/users/<id>', methods=['GET'])
def view(id):
    check_response = check_token()
    if check_response is False:
        return 'Unauthorized', 401

    if str(check_response['sub']) != str(id):
        return 'Forbidden', 403

    usuario = Usuario.query.get_or_404(id)

    return usuario_a_dict(usuario), 200


@blueprint.route('/users/<id>', methods=['PUT'])
def update(id):
    if check_token() is False:
        return 'Unauthorized', 401

    usuario = Usuario.query.get_or_404(id)
    datos = request.get_json()

    usuario.nombre = datos['nombre']
    usuario.password = datos['password']
    usuario.correo = datos['correo']

    db.session.add(usuario)
    db.session.commit()

    return usuario_a_dict(usuario), 200


@blueprint.route('/users/<id>', methods=['PATCH'])
def patch(id):
    if check_token() is False:
        return 'Unauthorized', 401

    usuario = Usuario.query.get_or_404(id)
    datos = request.get_json()

    usuario.nombre = datos.get('nombre', usuario.nombre)
    usuario.password = datos.get('password', usuario.password)
    usuario.correo = datos.get('correo', usuario.correo)

    db.session.add(usuario)
    db.session.commit()

    return usuario_a_dict(usuario), 200


@blueprint.route('/users/<id>', methods=['DELETE'])
def delete(id):
    if check_token() is False:
        return 'Unauthorized', 401

    usuario = Usuario.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    return '', 204


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    datos = request.get_json()

    correo = datos['correo']
    password = datos['password']

    usuario = Usuario.query.filter_by(correo=correo, password=password).first()

    if usuario is None:
        return 'Not found', 404

    payload = {
        'sub': usuario.id,
        'iat': datetime.datetime.now()
    }

    return jwt.encode(payload, '123456', algorithm='HS256')
