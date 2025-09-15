import os
import firebase_admin
from firebase_admin import credentials, firestore as admin_firestore
from google.cloud import firestore as gcloud_firestore

def get_db():
    """
    Devuelve la conexión a Firestore.
    - Si está el emulador activo -> conecta con google.cloud.firestore
    - Si no -> conecta a Firestore en la nube con firebase_admin
    """
    if os.getenv("FIRESTORE_EMULATOR_HOST"):
        print(" Conectado al Firestore Emulator:", os.getenv("FIRESTORE_EMULATOR_HOST"))
        return gcloud_firestore.Client(project="utte-471220")  # tu project-id
    else:
        if not firebase_admin._apps:
            cred = credentials.Certificate(
                os.path.join(os.path.dirname(__file__), "..", "keys", "utte-471220-427c3184644f.json")
            )
            firebase_admin.initialize_app(cred)

        print(" Conectado a Firestore en la nube")
        return admin_firestore.client()
