# Flask
from flask import Flask, jsonify, request, Response

# Flask-PyMongo
from flask_pymongo import PyMongo

# Utilities
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
""" 
generate_password_hash: Recibimos un string y lo ciframos
check_password_hash: verifica una contraseña

"""
app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/flaskmongodb'  # Configuracion para la direcciond e una base de datos
mongo=PyMongo(app)  # Conexion con MongoDB

@app.route('/users', methods=['POST'])
def create_user():
    """Endpoint Para creacion de usuarios"""
    username=request.json['username']
    email=request.json['email']
    password=request.json['password']

    if(username and email and password):
        hashed_password = generate_password_hash(password)
        """Creamos una nueva collecion en la DB y insetamos un nuevo documento"""
        user = mongo.db.users.insert_one({'username':username,'email':email,'password':hashed_password})
        # Otra forma es usar mongo.db.users.insert({'username':username,'email':email,'password':hashed_password}), que directamente nos retorna el id
        response = {
            'id':str(user.inserted_id),
            'username':username,
            'email':email,
            'password':hashed_password
        }
        return response
    else:
        return not_found()  # Mostramos el error de not_found

@app.route('/users' ,methods=['GET'])
def getUser():
    users = mongo.db.users.find()  # Devuelve una lista de objetos en formato Bson
    response = json_util.dumps(users)  # Convertimos los datos que estaban en Bson a tipo Json
    return Response(response, mimetype='application/json')  
    """Enviamos los datos, y especificamos una cabecera para establecer que se devolvera un json"""

@app.route('/users/<string:id>', methods=['GET'])
def retriveUser(id):
    objectID=ObjectId(id)  # Convertimos la cadena de id enviada a un objetoID de MongoDB
    user= mongo.db.users.find_one({"_id":objectID})  # Hacemos una busqueda por el ObjectID
    password= ch 
    respuesta={
        'mensaje':'Usuario encontrado',
        'user':user
    }  # Adicionando un mensaje a la respuesta devuelta
    response = json_util.dumps(user)  # Convertimos los datos a Json
    """Podemos no solo enviar lo que nos retorna Mongo, tambien podemos colocar algunos campos adicionales
    como el de respuesta, que contiene un mensaje extra. Esto directamente lo convertimos a Json con json_util.dump()
    """
    return Response(response, mimetype='application/json')

@app.route('/users/<string:id>',methods=['DELETE'])
def deleteUSer(id):
    mongo.db.users.delete_one({'_id':ObjectId(id)})  # Eliminado el objeto por su ObjID
    response = jsonify({
        'mensaje':'El usuario '+id+' fue eliminado exitosamente'
    })
    return response

@app.route('/users/<string:id>', methods=['PUT'])
def updateUser(id):
    user=mongo.db.users.find_one({'_id':ObjectId(id)})
    response = json_util.dumps(user)
    if(user):
        username=request.json.get('username',user['username'])
        email=request.json.get('email',user['email'])
        password=request.json['password']
        if username and email and password:
            hashedPassword = generate_password_hash(password)
            mongo.db.users.update_one({'_id':ObjectId(id)},{'$set':{
                'username':username,
                'email':email,
                'password':hashedPassword
            }})
            response = jsonify({'mensaje': 'el usuario '+id+' fue actualizado exitosamente'}) 
            return response
    else:
        return jsonify({'mensaje':'Usuario no encontrado'})
    # username=request.json.get('username',)
@app.errorhandler(404)  # Codigo de error que queremos manejar
def not_found(error=None):
    """Estas funciones sirven para que podamos controlar los errores
       de una forma que no se detenga nuestro servidor al momento
       que sucedan este tipo de errores."""
    response = jsonify({
        'mensaje':'Recurso no encontrado '+request.url,
        'status':404
    })
    response.status_code = 404
    return response
if __name__ == '__main__':
    app.run(debug=True, port=4000)
