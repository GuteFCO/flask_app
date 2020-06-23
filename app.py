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


@app.route('/')
def index():
    return '<h1>Hola</h1>'


@app.route('/register', methods=['POST'])
def register():
    datos = request.get_json()

    usuario = Usuario(**datos)

    db.session.add(usuario)
    db.session.commit()

    return {'id': 1, 'nombre': usuario.nombre}, 201


@app.route('/users', methods=['GET'])
def list():
    usuarios = Usuario.query.all()

    respuesta = []

    for usuario in usuarios:
        respuesta.append({
            'id': usuario.id,
            'nombre': usuario.nombre
        })

    return jsonify(respuesta), 200
