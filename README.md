# P2P Encrypted Chat Application

## Overview
This is a **Peer-to-Peer Encrypted Chat Application** that enables secure communication between users over a decentralized network. It employs **AES and RSA encryption** to ensure end-to-end security and uses **UDP-based peer discovery** for dynamic connections.

## Features
- **End-to-End Encryption:** Messages are encrypted using **AES (Fernet)**, and RSA keys (2048-bit) provide additional security.
- **Peer Discovery & Connection:** UDP broadcasting allows peers to dynamically find and connect with each other.
- **Persistent Chat History:** Stores encrypted messages in an **SQLite database (`chat_history.db`)**.
- **Multi-threaded Server:** Handles multiple clients simultaneously using TCP sockets.
- **Automatic Peer Monitoring:** Regularly checks for active peers and removes inactive ones.

## Encryption Mechanism
- **AES (Fernet Encryption):** Used for encrypting and decrypting chat messages securely.
- **RSA (Public/Private Key Encryption):** Provides key exchange and authentication.

## P2P Communication
- **UDP Broadcasting & Listening:** Peers broadcast their availability every **5 seconds**.
- **TCP Messaging:** Messages are transmitted securely over TCP sockets.
- **Peer List Management:** Peers are dynamically discovered and stored in **`peers.json`**.

## Database Management
- **SQLite Database (`chat_history.db`)** stores messages with timestamps for persistence.

## Multi-threaded Execution
- Runs parallel threads for:
  - **TCP server** (handling incoming messages)
  - **UDP peer discovery**
  - **Monitoring active peers**

## How to Use
### 1. Start a Peer
Run the script with a username and port:
```bash
python chat.py --name Alice --port 5000
```

### 2. Connect to Another Peer
Use option **4** in the menu to connect to a known peer.

### 3. Send Messages
Use option **1** to send a message to a peer.

### 4. View Chat History
Use option **3** to retrieve stored messages.

### 5. Check Active Peers
Use option **2** to list all discovered peers.

### 6. Exit the Chat
Type `exit` to disconnect from a peer.

## Requirements
Ensure you have the following dependencies installed:
```bash
pip install cryptography sqlite3 json socket threading argparse
```

