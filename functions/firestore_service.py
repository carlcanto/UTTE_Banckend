import bcrypt
from flask import jsonify
from .firebase_config import get_db 


def login(data):
    """
    Valida usuario contra Firestore.
    """
    db = get_db()
    users_ref = db.collection("users")

    cedula = data.get("cedula")
    password = data.get("password")

    if not cedula or not password:
        return {"status": "error", "message": "Faltan credenciales"}

    # Buscar usuario por cédula (usamos la cédula como ID del documento)
    user_doc = users_ref.document(cedula).get()

    if not user_doc.exists:
        return {"status": "error", "message": "Usuario no encontrado"}

    user_data = user_doc.to_dict()
    stored_hash = user_data.get("password")

    # Comparar contraseñas
    if not bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
        return {"status": "error", "message": "Contraseña incorrecta"}

    # Si todo bien
    return {
        "status": "success",
        "message": "Login exitoso",
        "user": {
            "cedula": user_data.get("cedula"),
            "nombre": user_data.get("nombre"),
            "email": user_data.get("email"),
        }
    }


def add_user(data):
    """
    Recibe un diccionario con los datos del usuario y lo guarda en Firestore.
    """
    db = get_db()
    users_ref = db.collection("users")

    cedula = data.get("cedula")
    password = data.get("password")
    nombre = data.get("nombre")
    email = data.get("email")

    # Validaciones
    if not cedula or not password or not nombre or not email:
        return {"status": "error", "message": "Faltan campos obligatorios"}

    # Revisar si ya existe un usuario con esa cédula
    existing_user = users_ref.document(cedula).get()
    if existing_user.exists:
        return {"status": "error", "message": "El usuario ya existe"}

    # Hashear la contraseña
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Guardar en Firestore (usamos cedula como ID del documento)
    users_ref.document(cedula).set({
        "cedula": cedula,
        "password": hashed_pw.decode("utf-8"),  # importante convertir a str
        "nombre": nombre,
        "email": email
    })

    return {"status": "success", "message": "Usuario creado correctamente"}

def delete_all_users():
    db = get_db()
    users_ref = db.collection("users")
    docs = users_ref.stream()

    deleted = 0
    for doc in docs:
        doc.reference.delete()
        deleted += 1

    return {"message": f"Se eliminaron {deleted} usuarios"}