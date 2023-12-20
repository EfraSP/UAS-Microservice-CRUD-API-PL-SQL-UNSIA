from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123123123@localhost/microservice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def encrypt_data(data, key):
    cipher = Cipher(algorithms.AES(key), modes.CFB(os.urandom(16)), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return urlsafe_b64encode(ciphertext)

def decrypt_data(encrypted_data, key):
    cipher = Cipher(algorithms.AES(key), modes.CFB(os.urandom(16)), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(urlsafe_b64decode(encrypted_data)) + decryptor.finalize()
    return decrypted_data

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    encrypted_password = db.Column(db.LargeBinary, nullable=False)

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data['username']
    password = data['password']

    key = os.urandom(32)
    encrypted_password = encrypt_data(password.encode(), key)

    new_user = User(username=username, encrypted_password=encrypted_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first()

    if user:
        decrypted_password = decrypt_data(user.encrypted_password, key)
        return jsonify({'username': user.username, 'password': decrypted_password.decode()})
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/user/<username>', methods=['PUT'])
def update_user(username):
    user = User.query.filter_by(username=username).first()

    if user:
        data = request.get_json()
        new_password = data['password']
        new_encrypted_password = encrypt_data(new_password.encode(), key)

        user.encrypted_password = new_encrypted_password
        db.session.commit()

        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/user/<username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()

    if user:
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
