from flask import Flask, request


app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hola</h1>'


@app.route('/register')
def register():
    datos = request.get_json()

    print(datos['nombre'])

    return '<h1>OK</h1>'
