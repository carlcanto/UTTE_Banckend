from flask import Flask, request, jsonify
from .firestore_service import login, delete_all_users, add_user
from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv() 

app = Flask(__name__)
CORS(app)

@app.route("/api/login", methods=["POST"])
def login_user():
    try:
        data = request.json
        result = login(data)
        return jsonify(result), 200 if result["status"] == "success" else 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route("/api/add_user", methods=["POST"])
def add_users():
    try:
        data = request.json
        result = add_user(data)
        return jsonify(result), 200 if result["status"] == "success" else 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/delete_user", methods=["DELETE"])
def delete_user_body():
    try:
        data = request.json
        user_id = data.get("user_id")
        
        if not user_id:
            return jsonify({"error": "Falta el campo user_id"}), 400

        db = get_db()
        user_ref = db.collection("users").document(user_id)

        if not user_ref.get().exists:
            return jsonify({"error": "El usuario no existe"}), 404

        user_ref.delete()
        return jsonify({"message": f"Usuario {user_id} eliminado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route("/api/delete_all_users", methods=["DELETE"])
def api_delete_all_users():
    # Seguridad: solo permitir esta acción si estamos en el emulador
    if not os.getenv("FIRESTORE_EMULATOR_HOST"):
        return jsonify({"error": "No permitido en producción"}), 403

    return jsonify(delete_all_users())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
