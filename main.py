import os
from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from pymongo import MongoClient
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)

mongo = os.environ['mongo']
otra = str(mongo)
client = MongoClient(otra)
cors = CORS(app, resources={r"/user/*": {"origins": "*"}})

@app.route('/', methods=['POST'])
def create_user():
    nombre = request.json['nombre']
    numero = request.json['numero']
    apellidos = request.json['apellidos']
    enfermedad = request.json['enfermedad']
    password = request.json['password']
    email = request.json['email']

    if nombre and numero and password and email:
        cifrado = generate_password_hash(password)
        id = client.db.users.insert_one({
            'nombre': nombre,
            'numero': numero,
            'apellidos': apellidos,
            'enfermeda': enfermedad,
            'password': cifrado,
            'email': email
        })
        response = {
            'id': str(id),
            'nombre': nombre,
            'numero': numero,
            'email': email,
            'apellidos': apellidos,
            'enfermeda': enfermedad,
            'password': cifrado,
        }
        return response
    else:
        {'message': 'No recibido'}

    return {'message': 'recibido'}


@app.route('/user', methods=['GET'])
def encontra():
    users = client.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')


@app.route('/user/<id>', methods=['GET'])
def consulta():
    #Para consulta los paccientes
    user = client.db.users.find_one({'_id:ObjectId(id)'})
    response = json_util()
    return "recibido"


@app.errorhandler(404)
def not_encontrado(error=None):
    message = jsonify({
        'message': 'Pagina no encontrada' + request.url,
        'status': 404
    })
    message.status_code = 404
    return message


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=81)
0
