# Peer-to-Peer Encrypted Chat Network

A decentralized peer-to-peer (P2P) encrypted chat system using Python, allowing secure communication between peers over a network.
**Also handles the bonus feature connecting to peers.**

## Features
- **Peer Discovery**: Uses UDP broadcasting to find and list active peers on the network.(Extra)
- **End-to-End Encryption**: Messages are encrypted using AES (Fernet) and RSA for secure transmission.
- **TCP-Based Communication**: Sends and receives encrypted messages using TCP sockets.
- **Chat History**: Stores messages in an SQLite database for retrieval.
- **Dynamic Peer Management**: Updates and maintains a list of connected peers.
- **Multi-Threaded Server**: Handles multiple connections simultaneously.
- **Automatic Peer Status Check**: Detects inactive peers and removes them.(Extra)

## Installation
### Prerequisites
Ensure you have Python installed along with the required dependencies.

```bash
pip install cryptography pycryptodome
pip install argparse
``` 
## Steps to run chat.py file
#### **Step 1: Run the Peer**  
To start a peer, use the following command:  

```bash
python peer_chat.py --name <YourName> --port <PortNumber>
```

For example:  

```bash
python peer_chat.py --name Alice --port 5000
python peer_chat.py --name Bob --port 5001
```

Each peer must have a **unique name** and **port number**.  

#### **Step 2: Using the Chat Application**  
Once the peer is running, you will see a menu:  

```
***** Menu *****
1. Send message  
2. Query active peers  
3. View chat history  
4. Connect to active peer  
0. Quit  
```

- **Option 1:** Enter the target peer's IP and port to send a message.  
- **Option 2:** View the list of currently active peers.  
- **Option 3:** Display saved chat history.  
- **Option 4:** Manually connect to another peer.  
- **Option 0:** Exit the application.  

#### **Step 3: Stopping a Peer**  
To stop a peer, type `"exit"` in the chat or press **Ctrl + C**.  

## How It Works
1. **Key Generation**: RSA and AES keys are generated for secure communication.
2. **Peer Discovery**: Peers broadcast their availability using UDP.
3. **Message Encryption**: Messages are encrypted before sending and decrypted upon receipt.
4. **Secure Communication**: Messages are transmitted over a TCP connection.
5. **Chat History**: All messages are stored locally in an SQLite database.

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

-1.Abhiraj Kumar(mc230041001).

-2.Harsh Bhati(mems230005017).

-3.Buradkar Kalyani Bhalchandra(cse230001017).
