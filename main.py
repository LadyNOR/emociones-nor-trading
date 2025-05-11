
from flask import Flask, request, jsonify
import ctypes
import os
from werkzeug.utils import secure_filename

# Cargar la librería Vokaturi
vokaturi = ctypes.CDLL("./libVokaturi.so")

# Definiciones de tipos y funciones
vokaturi.Vokaturi_open.restype = ctypes.c_void_p
vokaturi.Vokaturi_open.argtypes = [ctypes.c_int, ctypes.c_int]
vokaturi.Vokaturi_read_audio.restype = ctypes.c_int
vokaturi.Vokaturi_read_audio.argtypes = [
    ctypes.c_void_p,
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double)
]
vokaturi.Vokaturi_close.restype = None
vokaturi.Vokaturi_close.argtypes = [ctypes.c_void_p]

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/analizar-emocion", methods=["POST"])
def analizar_emocion():
    if "audio" not in request.files:
        return jsonify({"error": "No se proporcionó el archivo de audio"}), 400

    archivo = request.files["audio"]
    if archivo.filename == "":
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    nombre_seguro = secure_filename(archivo.filename)
    ruta_completa = os.path.join(UPLOAD_FOLDER, nombre_seguro)
    archivo.save(ruta_completa)

    # Simulación de análisis, porque el .so real necesita WAV crudo y normalizado
    emocion_detectada = "tristeza"  # <-- aquí puedes probar con emociones falsas

    return jsonify({"emocion": emocion_detectada})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
