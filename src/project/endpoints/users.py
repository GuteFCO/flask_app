from flask import request, jsonify, Blueprint
from project import db
from project.models import Usuario


blueprint = Blueprint('usuarios', __name__)


def usuario_a_dict(usuario):
    return {
        'id': usuario.id,
        'nombre': usuario.nombre,
        'correo': usuario.correo}


@blueprint.route('/register', methods=['POST'])
@blueprint.route('/users', methods=['POST'])
def register():
    datos = request.get_json()

    usuario = Usuario(**datos)

    db.session.add(usuario)
    db.session.commit()

    return usuario_a_dict(usuario), 201


@blueprint.route('/users', methods=['GET'])
def list():
    usuarios = Usuario.query.all()

    respuesta = []

    for usuario in usuarios:
        respuesta.append(usuario_a_dict(usuario))

    return jsonify(respuesta), 200


@blueprint.route('/users/<id>', methods=['GET'])
def view(id):
    usuario = Usuario.query.get_or_404(id)

    return usuario_a_dict(usuario), 200


@blueprint.route('/users/<id>', methods=['PUT'])
def update(id):
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
    usuario = Usuario.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    return '', 204
