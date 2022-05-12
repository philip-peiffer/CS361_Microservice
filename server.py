# NOTE - to run this application, you must first install the "cryptography" library

from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

# initialize the app
app = Flask(__name__)

# grab the key used to encrypt/decrypt or generate a new one if one doesn't exist
try:
    with open("key_file.txt", "r") as key_file:
        key = key_file.readline().encode()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open("key_file.txt", "w") as key_file:
        key_file.write(key.decode())


@app.before_request
def handle_content_type():
    if request.content_type != 'text/plain':
        return jsonify({"Error": "Content type must be text/plain"})


@app.route('/encrypt', methods=['POST'])
def encrypt_string():
    byte_str = request.data
    if len(byte_str) > 25:
        return jsonify({"Error": "Too long of a string. String must be less than 25 bytes long"})
    f = Fernet(key)

    # call Fernet method to encrypt
    enc_str = f.encrypt(byte_str)

    return enc_str


@app.route('/decrypt', methods=['POST'])
def decrypt_string():
    byte_str = request.data
    f = Fernet(key)

    # call Fernet method to decrypt
    dec_str = f.decrypt(byte_str)

    # decode from bytes to str and send this back
    dec_str = dec_str.decode()
    return dec_str


if __name__ == '__main__':
    app.run()
