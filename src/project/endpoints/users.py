import datetime
import jwt
import marshmallow
from functools import wraps
from flask import request, jsonify, Blueprint, current_app
from project import db, bcrypt
from project.models import Usuario
from project.schemas import usuario_schema, empresa_schema


blueprint = Blueprint('usuarios', __name__)


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
        return jwt.decode(token, current_app.config['SECRET'])
    except:
        return False


def autenticar(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        check_response = check_token()
        if check_response is False:
            return 'Unauthorized', 401
        return f(check_response, *args, **kwargs)
    return wrapper


@blueprint.route('/register', methods=['POST'])
@blueprint.route('/users', methods=['POST'])
def register():
    usuario = usuario_schema.load(request.json)

    db.session.add(usuario)
    db.session.commit()

    return usuario_schema.dump(usuario), 201


@blueprint.route('/users', methods=['GET'])
@autenticar
def list(payload):
    usuarios = Usuario.query.all()

    return jsonify(usuario_schema.dump(usuarios, many=True)), 200


@blueprint.route('/users/<id>', methods=['GET'])
@autenticar
def view(payload, id):
    if str(payload['sub']) != str(id):
        return 'Forbidden', 403

    usuario = Usuario.query.get_or_404(id)

    return usuario_schema.dump(usuario), 200


@blueprint.route('/users/<id>', methods=['PUT'])
@autenticar
def update(payload, id):
    usuario = Usuario.query.get_or_404(id)
    usuario = usuario_schema.load(
        data=request.json, instance=usuario, partial=False)

    db.session.add(usuario)
    db.session.commit()

    return usuario_schema.dump(usuario), 200


@blueprint.route('/users/<id>', methods=['PATCH'])
@autenticar
def patch(payload, id):
    usuario = Usuario.query.get_or_404(id)
    usuario = usuario_schema.load(
        data=request.json, instance=usuario, partial=True)

    db.session.add(usuario)
    db.session.commit()

    return usuario_schema.dump(usuario), 200


@blueprint.route('/users/<id>', methods=['DELETE'])
@autenticar
def delete(payload, id):
    usuario = Usuario.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    return '', 204


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    datos = request.get_json()

    correo = datos['correo']
    password = datos['password']

    usuario = Usuario.query.filter_by(correo=correo).first()

    if usuario is None:
        return 'Not found', 404

    if bcrypt.check_password_hash(usuario.password, password) is False:
        return 'Not found', 404

    payload = {
        'sub': usuario.id,
        'name': usuario.nombre,
        'iat': datetime.datetime.now()
    }

    return jwt.encode(
        payload,
        current_app.config['SECRET'],
        algorithm='HS256')


@blueprint.route('/token', methods=['GET'])
@autenticar
def usuario(payload):
    usuario = Usuario.query.get_or_404(payload['sub'])

    return usuario_schema.dump(usuario), 200
