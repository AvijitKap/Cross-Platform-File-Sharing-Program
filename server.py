from flask import Flask, request, send_from_directory, render_template, jsonify
import os
import socket
import pyqrcode

app = Flask(__name__)

# 🗂 Folder where uploaded files are stored
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if not exists
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 🌍 Get the local IP address dynamically
def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception as e:
        print(f"❌ Error getting local IP: {e}")
        return "127.0.0.1"  # Fallback to localhost if an error occurs

# 📁 Define Static Folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get current script location
STATIC_FOLDER = os.path.join(BASE_DIR, "static")
os.makedirs(STATIC_FOLDER, exist_ok=True)  # Ensure static folder exists

# 🌐 Generate QR Code
local_ip = get_local_ip()
url = f"http://{local_ip}:5000"  # Flask server URL
qr_path = os.path.join(STATIC_FOLDER, "qrcode.png")

try:
    qr = pyqrcode.create(url)
    qr.png(qr_path, scale=8)

    if os.path.exists(qr_path):
        print(f"✅ QR Code saved successfully at: {qr_path} (for {url})")
    else:
        print("❌ QR Code generation failed!")
except Exception as e:
    print(f"❌ Error generating QR Code: {e}")

# 🌍 Serve Web UI
@app.route("/")
def index():
    return render_template("index.html", local_ip=local_ip)

# 🖼 Serve QR Code
@app.route("/qrcode.png")
def serve_qr_code():
    return send_from_directory(STATIC_FOLDER, "qrcode.png")

# 📂 Upload Multiple Files
@app.route("/upload", methods=["POST"])
def upload_file():
    if "files[]" not in request.files:
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist("files[]")

    if not files or files[0].filename == "":
        return jsonify({"error": "No selected file"}), 400

    for file in files:
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))

    return jsonify({"message": "Files uploaded successfully!"})

# 📜 List Available Files
@app.route("/files")
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify(files)

# 📥 Download Files
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# 🚀 Run Flask Server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
