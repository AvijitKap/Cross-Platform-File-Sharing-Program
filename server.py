from flask import Flask, request, send_file, render_template, jsonify
import os
import socket
import pyqrcode
import io
import secrets
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 🌍 Get dynamic local IP address
def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception as e:
        print(f"❌ Error getting local IP: {e}")
        return "127.0.0.1"

# 🔐 Generate encryption key from password
def derive_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# 🔒 Encrypt file
def encrypt_file(file_path, password):
    salt = secrets.token_bytes(16)
    key = derive_key(password, salt)
    iv = secrets.token_bytes(16)

    with open(file_path, "rb") as f:
        plaintext = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    pad_length = 16 - (len(plaintext) % 16)
    padded_plaintext = plaintext + bytes([pad_length]) * pad_length

    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    encrypted_data = salt + iv + ciphertext

    with open(file_path, "wb") as f:
        f.write(encrypted_data)

# 🔓 Decrypt file
def decrypt_file(file_path, password):
    with open(file_path, "rb") as f:
        data = f.read()

    salt = data[:16]
    iv = data[16:32]
    ciphertext = data[32:]

    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

    pad_length = decrypted_padded[-1]
    decrypted = decrypted_padded[:-pad_length]

    return decrypted

# 🌐 Generate QR Code dynamically
@app.route("/qrcode")
def generate_qr_code():
    local_ip = get_local_ip()
    url = f"http://{local_ip}:5000"
    qr = pyqrcode.create(url)

    buffer = io.BytesIO()
    qr.png(buffer, scale=8)
    buffer.seek(0)

    return send_file(buffer, mimetype="image/png")

# 🌍 Serve Web UI
@app.route("/")
def index():
    return render_template("index.html", local_ip=get_local_ip())

# 📂 Upload and Encrypt Files
@app.route("/upload", methods=["POST"])
def upload_file():
    if "files[]" not in request.files or "password" not in request.form:
        return jsonify({"error": "Missing files or password"}), 400

    files = request.files.getlist("files[]")
    password = request.form["password"]

    if not files or files[0].filename == "":
        return jsonify({"error": "No selected file"}), 400

    for file in files:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        encrypt_file(file_path, password)

    return jsonify({"message": "Files uploaded & encrypted successfully!"})

# 📜 List Available Files
@app.route("/files")
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify(files)

# 📥 Decrypt & Download Files
@app.route("/download/<filename>", methods=["POST"])
def download_file(filename):
    password = request.form.get("password")

    if not password:
        return jsonify({"error": "Password is required"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        decrypted_data = decrypt_file(file_path, password)

        return decrypted_data, 200, {
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "application/octet-stream"
        }

    except Exception:
        return jsonify({"error": "Incorrect password or file corrupted"}), 400

# 🚀 Run Flask Server
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "App Working on Vercel"

