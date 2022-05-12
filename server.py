# NOTE - to run this application, you must first install the "cryptography" library

from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

# initialize the app
app = Flask(__name__)

# generate the key that will be used to encrypt/decrypt.
key = Fernet.generate_key()


@app.post('/encrypt')
def encrypt_string():
    if request.content_type != 'text/plain':
        return jsonify({"Error": "Content type must be text/plain"})

    byte_str = request.data
    if len(byte_str) > 25:
        return jsonify({"Error": "Too long of a string. String must be less than 25 bytes long"})
    f = Fernet(key)

    # call Fernet method to encrypt
    enc_str = f.encrypt(byte_str)

    return enc_str


@app.post('/decrypt')
def decrypt_string():
    if request.content_type != 'text/plain':
        return jsonify({"Error": "Content type must be text/plain"})

    byte_str = request.data
    f = Fernet(key)

    # call Fernet method to decrypt
    dec_str = f.decrypt(byte_str)

    # decode from bytes to str and send this back
    dec_str = dec_str.decode()
    return dec_str


if __name__ == '__main__':
    app.run()
