from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from config import ApplicationConfig
from flask_session import Session
import secrets
from routes.user import reg_user
from routes.not_found import not_found
     

app = Flask(__name__)
Bcrypt = Bcrypt(app)

app.secret_key = ApplicationConfig.SECRET_KEY
server_session = Session(app)
user_collection = ApplicationConfig.DB['user'] #collection name : user
        


@app.route('/user/register', methods=['POST'])
def add_user():
  resp = reg_user(user_collection, request)
  return resp
  

@app.route('/login', methods=['POST'])
def login():
  _json =request.json
  _email = _json['email']
  _password = _json['password']
  user = user_collection.find_one({'email':_email})
  if user:
    if check_password_hash(user['password'], _password) :
      resp = dumps(user)
      #session["user_id"] = user['_id']
      return resp
      
    else:
      resp = jsonify("Email or password invalid")
      return resp
  else:
    resp = jsonify("Email or password invalid")
    return resp


@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
  user_collection.delete_one({'_id':ObjectId(id)})
  resp = jsonify("User deleted succesfully!")
  resp.status_code = 200

  return resp


@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
  _id = id
  _json =request.json
  _name = _json['name']
  _email = _json['email']
  _pwd = _json['pwd']
  if _name and _email and _pwd and _id and request.method == 'POST':
    _hashed_password = generate_password_hash(_pwd)
    user_collection.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name': _name , 'email' : _email, 'pwd' : _hashed_password}} )
    resp = jsonify("User updated succesfully!")
    resp.status_code = 200

    return resp
  else:
    return not_found

if __name__ == "__main__" :
    app.run(debug=True)
    
