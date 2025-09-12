from flask import Flask, request, jsonify
from flask_cors import CORS
from firestore_service import add_user, get_user

app = Flask(__name__)
CORS(app)

@app.route("/api/add_user", methods=["POST"])
def api_add_user():
    data = request.json
    cedula = data.get("cedula")
    password = data.get("password")
    if not cedula or not password:
        return jsonify({"error": "Cédula y contraseña requeridas"}), 400
    return jsonify(add_user(cedula, password))

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json
    cedula = data.get("cedula")
    password = data.get("password")
    if not cedula or not password:
        return jsonify({"error": "Cédula y contraseña requeridas"}), 400
    return jsonify(get_user(cedula, password))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
