import os
import firebase_admin
from firebase_admin import credentials, firestore as admin_firestore
from google.cloud import firestore as gcloud_firestore

# Inicializa Firebase solo si no está ya inicializado
if not firebase_admin._apps and not os.getenv("FIRESTORE_EMULATOR_HOST"):
    cred = credentials.Certificate(
        os.path.join(os.path.dirname(__file__), "..", "keys", "utte-471220-427c3184644f.json")
    )
    firebase_admin.initialize_app(cred)

def get_db():
    """
    Devuelve la conexión a Firestore.
    - Si está el emulador activo -> conecta con google.cloud.firestore
    - Si no -> conecta a Firestore en la nube con firebase_admin
    """
    if os.getenv("FIRESTORE_EMULATOR_HOST"):
        print("🔥 Conectado al Firestore Emulator:", os.getenv("FIRESTORE_EMULATOR_HOST"))
        return gcloud_firestore.Client(project="utte-471220")  # tu project-id
    else:
        print("☁️ Conectado a Firestore en la nube")
        return admin_firestore.client()


def add_user(cedula, password):
    db = get_db()
    users_ref = db.collection("users")
    user_doc = users_ref.document(cedula)
    user_doc.set({
        "cedula": cedula,
        "password": password
    })
    return {"message": "Usuario agregado con éxito", "cedula": cedula}


def get_user(cedula, password):
    db = get_db()
    user_ref = db.collection("users").document(cedula).get()
    if user_ref.exists:
        user = user_ref.to_dict()
        if user["password"] == password:
            return {"status": "success", "user": user}
        else:
            return {"status": "error", "message": "Contraseña incorrecta"}
    else:
        return {"status": "error", "message": "Usuario no encontrado"}
