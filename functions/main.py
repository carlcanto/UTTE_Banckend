from firebase_functions import https_fn
from firebase_admin import initialize_app
from flask import Flask, request, jsonify

# Inicializa el Firebase Admin SDK.
# Esto es buena práctica si vas a interactuar con otros servicios de Firebase
# (como Firestore, Realtime Database, Authentication) desde tu función.
initialize_app()

# Crea tu aplicación Flask
app = Flask(__name__)

# Define tus rutas de Flask
@app.route('/')
def hello_world():
    return "¡Hola desde Flask dentro de una Firebase Cloud Function emulada!"

@app.route('/saludar')
def greet_user():
    name = request.args.get('nombre', 'Mundo')
    return f"¡Saludos, {name}, desde Flask!"

@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'GET':
        return jsonify({"mensaje": "Esto es una petición GET a /api/data"})
    elif request.method == 'POST':
        # Asume que el cuerpo de la petición es JSON
        data = request.json
        return jsonify({"recibido": data, "mensaje": "Datos POST recibidos"})
    return "Método no permitido", 405

# Exponemos la aplicación Flask como una Cloud Function HTTP.
# La librería firebase_functions maneja automáticamente la integración
# de aplicaciones WSGI (como Flask). Simplemente retornamos la instancia de 'app'.
@https_fn.on_request()
def flask_api(_: https_fn.Request):
    """
    Función HTTP de Cloud que enruta las peticiones a una aplicación Flask.
    El decorador `https_fn.on_request` espera que retornemos la instancia
    de la aplicación Flask, y él se encarga del resto.
    """
    return app