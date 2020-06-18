from flask import Flask, request


app = Flask(__name__)


class Usuario:
    def __init__(self, nombre, password, confirmacion):
        self.nombre = nombre
        self.password = password


@app.route('/')
def index():
    return '<h1>Hola</h1>'


@app.route('/register', methods=['POST'])
def register():
    datos = request.get_json()

    usuario = Usuario(**datos)

    return {'id': 1, 'nombre': usuario.nombre}, 201
