import os
from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from pymongo import MongoClient
import pymongo
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
from flask_cors import CORS



app = Flask(__name__)

mongo = os.environ['mongo']
otra = str(mongo)
client = MongoClient(otra)
cors = CORS(app, resources={r"/user/*": {"origins": "*"}})

app.config["UPLOAD_FOLDER"] = "archivos"
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'gif','pdf','txt','doc','docx'])


def extesiones(file):
  file = file.split('.')
  if file[1] in ALLOWED_EXTENSIONS:
    return True
  return False


@app.route('/user/crear', methods=['POST'])
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
def consulta(id):
  #Para consulta los paccientes
  user = client.db.users.find_one({'_id':ObjectId(id)})
  if(len(user)>0):
    response = json_util.dumps(user)
    return response
  return jsonify({"message":"no encontrado"})


@app.route('/user/<id>', methods=['DELETE'])
def userDel(id):
  client.db.users.delete_one({'_id':ObjectId(id)})
  response= jsonify({"message":"user" +  id + " ha sido eliminado"})
  return response



@app.route('/user/archivos', methods=['POST'])
def guardaArchivo():
  file = request.file["uploadFile"]
  filename = secure_filename(file.filename)
  if file and extesiones(filename):
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    return jsonify({"message":"Subido correctamente"})
  return jsonify({"message":"No subido"})


@app.errorhandler(404)
def not_encontrado(error=None):
  message = jsonify({
    'message': 'Pagina no encontrada' + request.url,
    'status': 404
  })
  message.status_code = 404
  return message

@app.errorhandler(403)
def not_encontrado(error=None):
  message = jsonify({
    'message': 'acceso no permitido',
    'status': 403
  })
  message.status_code = 403
  return message

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=81)
0
