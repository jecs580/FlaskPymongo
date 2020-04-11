# Flask
from flask import Flask, jsonify, request

# Flask-PyMongo
from flask_pymongo import PyMongo

# Utilities
from werkzeug.security import generate_password_hash, check_password_hash
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

@app.errorhandler(404)  # Codigo de error que queremos manejar
def not_found(error=None):
    """Estas funciones sirven para que podamos controlar
       de una forma que no se tire nuestro servidor al momento
       que sucedan este tipo de errores."""
    response={
        'mensaje':'Recurso no encontrado '+request.url,
        'status':404
    }
    return response
if __name__ == '__main__':
    app.run(debug=True, port=4000)
    