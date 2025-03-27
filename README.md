<h1 align="center">🚀 Cross-Platform File Sharing</h1>

<p align="center">
  A simple & efficient file-sharing web app using <b>Flask</b>. <br>
  Upload, list, and download files easily over a local network. <br>
  A <b>QR Code</b> is generated dynamically to help users access the platform on mobile devices..
</p>

---

## 🔥 Features

✅ Upload multiple files at once  
✅ Drag & Drop support for easy file uploads  
✅ Download files from any connected device  
✅ Auto-generated **QR Code** for quick access  
✅ Responsive UI with **Bootstrap**  

---

## 📦 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YourGitHubUsername/cross-file-sharing.git
cd cross-file-sharing
```

### 2️⃣ Install Dependencies
```bash
pip install flask qrcode pyqrcode pillow
```

### 3️⃣ Run the Application
```bash
python app.py
```

🚀 The server will start at **http://your-local-ip:5000**

---

## 📲 Access on Mobile
📌 **Scan the QR Code** displayed on the web UI or manually enter **http://your-local-ip:5000** in your phone’s browser.


---

## 📜 API Endpoints

| Endpoint           | Method | Description                        |
|--------------------|--------|------------------------------------|
| `/`               | GET    | Load the main web UI              |
| `/upload`         | POST   | Upload one or multiple files      |
| `/files`          | GET    | List all uploaded files           |
| `/download/<filename>` | GET    | Download a specific file         |

---

## 🎨 Tech Stack
<p align="center">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white">
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
  <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white">
</p>
