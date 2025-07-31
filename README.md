# 🔐 Encrypted File Transfer System

A secure client-server system for encrypted file transfer using socket communication, asymmetric encryption (RSA), and symmetric encryption (AES).  
The server is implemented in **C++**, and the client is implemented in **Python**.

---

## 📁 Project Structure

```
root/
│
├── client/                      # Python-based client
│   ├── main.py                  # Entry point for client
│   ├── helper.py                # Utility functions
│   ├── request.py               # Request formatting
│   ├── response.py              # Response handling
│   ├── request_handler.py       # Logic for sending/receiving
│   └── test.py                  # Basic testing
│
├── AESWrapper.cpp/.h           # AES encryption wrapper
├── RSAWrapper.cpp/.h           # RSA encryption wrapper
├── Base64Wrapper.cpp/.h        # Base64 encoding/decoding
├── ClientHelper.cpp/.h         # General C++ utilities
├── handel_socket.cpp/.h        # Socket handling functions
├── protocol.cpp/.h             # Protocol definitions
├── main.cpp                    # Server entry point
└── rsa_key.h                   # Key management
```

---

## 🚀 How to Run

### 🔧 Server (C++)

1. Compile using `g++` or any C++ compiler (example):
   ```bash
   g++ main.cpp AESWrapper.cpp RSAWrapper.cpp Base64Wrapper.cpp \
       ClientHelper.cpp handel_socket.cpp protocol.cpp -o server
   ```

2. Run:
   ```bash
   ./server
   ```

---

### 💻 Client (Python)

1. Navigate to the `client` folder:
   ```bash
   cd client
   ```

2. Run:
   ```bash
   python main.py
   ```

---

## 🔐 Technologies Used

- **C++** – Server implementation, encryption logic
- **Python** – Client logic and communication
- **Sockets** – TCP-based communication between client and server
- **RSA / AES** – Secure encryption for data exchange
- **Base64** – Encoding binary data for transmission

---

## 📌 Features

- End-to-end encrypted file transfer
- Use of asymmetric and symmetric encryption for security
- Clean protocol abstraction
- Modular and maintainable structure
- Written in two languages to demonstrate cross-language communication

---

## 📎 Author

**Racheli Wizel**  
[LinkedIn](https://www.linkedin.com/in/racheli-wizel1) | [GitHub](https://github.com/RacheliWizel/secure-file-transfer)
