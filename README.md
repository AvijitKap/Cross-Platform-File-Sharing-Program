# 🔐 Secure File Sharing with Password Encryption

A simple and secure Flask web app that allows users to **upload, encrypt, download, and decrypt files** using a **password**. It also provides a **QR code** to access the app locally on other devices like your phone.

---

## 🚀 Features

- 🔒 AES Encryption/Decryption using user-defined password
- 📤 Upload multiple files and encrypt them on the server
- 📥 Download files after secure decryption
- 🌐 Access from other devices via QR code and local IP
- 🧠 Flask backend with Bootstrap 5 frontend
- 🔐 PBKDF2HMAC key derivation with random salt for each file

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/secure-file-sharing.git
cd secure-file-sharing
```

### 2. Create a Virtual Environment (Optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install flask pyqrcode cryptography
```

---

## ▶️ Run the App

```bash
python app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

Or scan the QR code to access from your phone.

---

## 📂 Project Structure

```
secure-file-sharing/
├── app.py
├── templates/
│   └── index.html
├── uploads/                # Stores encrypted files

```

---

## 📦 API Endpoints

| Endpoint                | Method | Description                      |
|-------------------------|--------|----------------------------------|
| `/`                     | GET    | Main web UI                      |
| `/upload`               | POST   | Upload and encrypt files         |
| `/files`                | GET    | List all uploaded files          |
| `/download/<filename>`  | POST   | Decrypt and download a file      |
| `/qrcode`               | GET    | Get QR code for local access     |

---

## 🔑 How It Works

- File is encrypted with AES-CBC using a key derived from the password.
- A random `salt` and `IV` are generated per file.
- Encrypted data = `salt + iv + ciphertext`.
- Files are decrypted using the same password.
- If password is incorrect, decryption fails.

---

## 🔐 Security Notes

- Passwords are never stored anywhere.
- Files are encrypted in-place using AES with PKCS7 padding.
- Derived keys use SHA-256 and 100,000 PBKDF2 iterations.

---

## ✅ Future Improvements

- 🧾 File metadata preview
- 🗑️ File delete option
- 🔃 Drag and drop support
- 🔁 Real-time socket updates

---

## 📄 License

Licensed under the MIT License.

---

Made with ❤️ by [Avijit]
