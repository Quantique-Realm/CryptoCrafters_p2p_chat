# Peer-to-Peer Encrypted Chat Network

A decentralized peer-to-peer (P2P) encrypted chat system using Python, allowing secure communication between peers over a network.

## Features
- **Peer Discovery**: Uses UDP broadcasting to find and list active peers on the network.
- **End-to-End Encryption**: Messages are encrypted using AES (Fernet) and RSA for secure transmission.
- **TCP-Based Communication**: Sends and receives encrypted messages using TCP sockets.
- **Chat History**: Stores messages in an SQLite database for retrieval.
- **Dynamic Peer Management**: Updates and maintains a list of connected peers.
- **Multi-Threaded Server**: Handles multiple connections simultaneously.
- **Automatic Peer Status Check**: Detects inactive peers and removes them.

## Installation
### Prerequisites
Ensure you have Python installed along with the required dependencies.

```bash
pip install cryptography pycryptodome
pip install argparse
```

### Running the Peer
Each user (peer) must specify their name and port to start the chat.

```bash
python peer_chat.py --name "YourName" --port 5000
```

## How It Works
1. **Key Generation**: RSA and AES keys are generated for secure communication.
2. **Peer Discovery**: Peers broadcast their availability using UDP.
3. **Message Encryption**: Messages are encrypted before sending and decrypted upon receipt.
4. **Secure Communication**: Messages are transmitted over a TCP connection.
5. **Chat History**: All messages are stored locally in an SQLite database.

## Usage
### Menu Options
Once the program starts, the following options are available:
- **Send message**: Send an encrypted message to another peer.
- **Query active peers**: List currently active peers.
- **View chat history**: Retrieve stored messages from the database.
- **Connect to a peer**: Establish a connection with a specific peer.
- **Exit**: Stop the program and disconnect from the network.

## File Structure
```
📂 PeerChat
 ├── chat.py        # Main script for peer-to-peer communication
 ├── secret.key          # AES encryption key
 ├── private.pem         # RSA private key
 ├── public.pem          # RSA public key
 ├── peers.json          # Stores discovered peers
 ├── chat_history.db     # SQLite database for storing chat messages
```

## Security
- **AES Encryption**: Messages are encrypted using AES (Fernet) for confidentiality.
- **RSA Encryption**: RSA is used for secure key exchanges.
- **Peer Authentication**: Peers must identify themselves using a team name.
- **Encrypted Broadcasts**: UDP discovery messages are encrypted to prevent spoofing.
  
**Output Screenshots**
## Terminal 1
![WhatsApp Image 2025-02-21 at 4 31 20 PM](https://github.com/user-attachments/assets/2571a623-e6c2-4fa9-a9c7-79a352ee9e5d)
![WhatsApp Image 2025-02-21 at 4 32 53 PM](https://github.com/user-attachments/assets/f3a11b90-7dc4-472a-906e-249845a53155)

## Terminal 2
![WhatsApp Image 2025-02-21 at 4 41 48 PM](https://github.com/user-attachments/assets/fb27c4de-f874-4b3e-88af-0f760cda5f1e)

## Terminal 3
![WhatsApp Image 2025-02-21 at 4 42 38 PM](https://github.com/user-attachments/assets/4bf9fdbd-30bb-4035-aa76-7af15395601d)

---
Developed by **CryptoCrafters** 
-1.Abhiraj Kumar.
-2.Harsh Bhati.
-3.Buradkar Kalyani Bhalchandra.
