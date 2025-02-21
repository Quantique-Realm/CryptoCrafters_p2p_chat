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
 ├── peer_chat.py        # Main script for peer-to-peer communication
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

## Future Improvements
- **File Sharing**: Add functionality to securely send and receive files.
- **GUI Interface**: Develop a graphical interface for better user experience.
- **Group Chat**: Support multi-user chat rooms.
- **Mobile Support**: Expand functionality to mobile devices.

## Contributing
Pull requests are welcome! If you find a bug or have suggestions, feel free to create an issue.

## License
This project is licensed under the MIT License.

---
Developed by **CryptoCrafters** 🚀
