import socket
import threading
import argparse
import json
import os
import time
import sqlite3
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Constants
KEY_FILE = "secret.key"
PRIVATE_KEY_FILE = "private.pem"
PUBLIC_KEY_FILE = "public.pem"
PEERS_FILE = "peers.json"
CHAT_DB = "chat_history.db"
UDP_PORT = 54545
TEAM_NAME = "CryptoCrafters"  # Hardcoded team name

# Generate or load encryption key
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
else:
    with open(KEY_FILE, "rb") as key_file:
        key = key_file.read()
encryptor = Fernet(key)

# RSA Key Generation
if not os.path.exists(PRIVATE_KEY_FILE):
    rsa_key = RSA.generate(2048)
    with open(PRIVATE_KEY_FILE, "wb") as private_file:
        private_file.write(rsa_key.export_key())
    with open(PUBLIC_KEY_FILE, "wb") as public_file:
        public_file.write(rsa_key.publickey().export_key())
else:
    with open(PRIVATE_KEY_FILE, "rb") as private_file:
        rsa_key = RSA.import_key(private_file.read())
rsa_cipher = PKCS1_OAEP.new(rsa_key)

# Database Setup
def init_db():
    conn = sqlite3.connect(CHAT_DB)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages 
                      (id INTEGER PRIMARY KEY, sender TEXT, message TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

init_db()

def save_message(sender, message):
    conn = sqlite3.connect(CHAT_DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender, message, timestamp) VALUES (?, ?, ?)",
                   (sender, message, time.ctime()))
    conn.commit()
    conn.close()

def load_peers():
    if os.path.exists(PEERS_FILE):
        with open(PEERS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_peers(peers):
    with open(PEERS_FILE, "w") as file:
        json.dump(peers, file, indent=4)

class Peer:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.peers = load_peers()
        self.running = True
        threading.Thread(target=self.start_server, daemon=True).start()
        threading.Thread(target=self.udp_broadcast, daemon=True).start()
        threading.Thread(target=self.udp_listener, daemon=True).start()
        threading.Thread(target=self.check_peer_status, daemon=True).start()

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", self.port))
        server.listen(5)
        print(f"Server listening on port {self.port}...")
        while self.running:
            try:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr), daemon=True).start()
            except Exception as e:
                print("Server Error:", e)

    def handle_client(self, client, addr):
        ip, port = addr
        while self.running:
            try:
                message = client.recv(1024)
                if not message:
                    break
                decrypted_message = encryptor.decrypt(message).decode()
                # Parse the message
                sender_ip_port, sender_team_name, msg = decrypted_message.split(maxsplit=2)
                print(f"{sender_ip_port} {sender_team_name} {msg}")
                save_message(sender_ip_port, msg)
                # Avoid duplicate entries
                if sender_ip_port not in self.peers:
                    self.peers[sender_ip_port] = (ip, port)
                    save_peers(self.peers)
                # Handle "exit" message
                if msg.strip().lower() == "exit":
                    print(f"{sender_ip_port} disconnected.")
                    del self.peers[sender_ip_port]
                    save_peers(self.peers)
                    break
            except Exception as e:
                print("Connection Error:", e)
                break
        client.close()

    def send_message(self, target_ip, target_port, message):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((target_ip, target_port))
            # Format the message as per the requirement
            formatted_message = f"{socket.gethostbyname(socket.gethostname())}:{self.port} {TEAM_NAME} {message}"
            encrypted_message = encryptor.encrypt(formatted_message.encode())
            client.send(encrypted_message)
            self.peers[f"{target_ip}:{target_port}"] = (target_ip, target_port)
            save_peers(self.peers)
            print(f"Message sent to {target_ip}:{target_port}")
        except Exception as e:
            print(f"Failed to connect to {target_ip}:{target_port} - {e}")
        finally:
            client.close()

    def connect_to_peer(self, target_ip, target_port):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((target_ip, target_port))
            # Send a connection message
            connection_message = f"{socket.gethostbyname(socket.gethostname())}:{self.port} {TEAM_NAME} Connection established"
            encrypted_message = encryptor.encrypt(connection_message.encode())
            client.send(encrypted_message)
            self.peers[f"{target_ip}:{target_port}"] = (target_ip, target_port)
            save_peers(self.peers)
            print(f"Connected to {target_ip}:{target_port}")
        except Exception as e:
            print(f"Failed to connect to {target_ip}:{target_port} - {e}")
        finally:
            client.close()

    def udp_broadcast(self):
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        message = f"{self.name}:{self.port}"
        while self.running:
            udp_sock.sendto(encryptor.encrypt(message.encode()), ('<broadcast>', UDP_PORT))
            time.sleep(5)

    def udp_listener(self):
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_sock.bind(("", UDP_PORT))
        last_seen = {}
        while self.running:
            try:
                data, addr = udp_sock.recvfrom(1024)
                peer_info = encryptor.decrypt(data).decode().split(":")
                if len(peer_info) != 2:
                    continue
                peer_name, peer_port = peer_info
                peer_ip = addr[0]
                peer_port = int(peer_port)
                if f"{peer_ip}:{peer_port}" in self.peers:
                    continue
                current_time = time.time()
                if peer_ip in last_seen and current_time - last_seen[peer_ip] < 10:
                    continue
                self.peers[f"{peer_ip}:{peer_port}"] = (peer_ip, peer_port)
                last_seen[peer_ip] = current_time
                save_peers(self.peers)
                print(f"Discovered peer {peer_name} at {peer_ip}:{peer_port}")
            except Exception as e:
                print(f"UDP Listener Error: {e}")

    def check_peer_status(self):
        while self.running:
            time.sleep(10)
            for peer_ip_port in list(self.peers.keys()):
                ip, port = self.peers[peer_ip_port]
                if not self.is_peer_active(ip, port):
                    print(f"Peer {peer_ip_port} is offline.")
                    del self.peers[peer_ip_port]
                    save_peers(self.peers)

    def is_peer_active(self, ip, port):
        try:
            sock = socket.create_connection((ip, port), timeout=2)
            sock.close()
            return True
        except:
            return False

    def start(self):
        while self.running:
            print("\n***** Menu *****")
            print("1. Send message")
            print("2. Query active peers")
            print("3. View chat history")
            print("4. Connect to active peers")
            print("0. Quit")
            choice = input("Enter choice: ")
            if choice == "1":
                target_ip = input("Enter recipient's IP: ")
                target_port = int(input("Enter recipient's port number: "))
                message = input("Enter your message: ")
                self.send_message(target_ip, target_port, message)
            elif choice == "2":
                self.query_active_peers()
            elif choice == "3":
                conn = sqlite3.connect(CHAT_DB)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM messages")
                for row in cursor.fetchall():
                    print(row)
                conn.close()
            elif choice == "4":
                target_ip = input("Enter peer's IP: ")
                target_port = int(input("Enter peer's port number: "))
                self.connect_to_peer(target_ip, target_port)
            elif choice == "0":
                self.running = False
                break

    def query_active_peers(self):
        print("Connected Peers:")
        for peer_ip_port in self.peers:
            print(peer_ip_port)
        if not self.peers:
            print("No connected peers")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True, help="Name of the peer")
    parser.add_argument("--port", type=int, required=True, help="Port number for the peer")
    args = parser.parse_args()
    peer = Peer(args.name, args.port)
    peer.start()