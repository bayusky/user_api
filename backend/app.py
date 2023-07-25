from flask import Flask, jsonify, request
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from config import ApplicationConfig
from flask_session import Session
import secrets
from mail import mailer
     

app = Flask(__name__)

app.secret_key = ApplicationConfig.SECRET_KEY
server_session = Session(app)
user_collection = ApplicationConfig.DB['user'] #collection name : user
        


@app.route('/users', methods=['GET'])
def users():
  users = user_collection.find()
  resp = dumps(users)
  return resp

@app.route('/register', methods=['POST'])
def add_user():
  _json =request.json
  _name = _json['name']
  _email = _json['email']
  _password = _json['password']

  if _name and _email and _password and request.method == 'POST':
    _hashed_password = generate_password_hash(_password)
    print(_hashed_password)
    existing_mail = user_collection.find_one({'email': _email})
    if existing_mail:
      resp = jsonify("Email exist!")
      return(resp)
    else:
      verify_token = secrets.token_urlsafe(30*3//4)
      user_collection.insert_one({'name': _name , 'email' : _email, 'password' : _hashed_password, 'verify_token': verify_token})
      flag = "register"
      mailer(_email, verify_token, flag)

      resp = jsonify("User added succesfully!")
      resp.status_code = 200

      return resp
  else:
    return not_found()

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

@app.errorhandler(404)
def not_found(error=None):
  message = {
    'status' : 404,
    'message' : 'Not Found' + request.url
  }
  resp = jsonify(message)
  resp.status_code = 404
  return resp

if __name__ == "__main__" :
    app.run(debug=True)
    
