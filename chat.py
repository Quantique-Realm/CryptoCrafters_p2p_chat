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

# Broadcast IP can be customized to target a specific network segment.
# For LAN, "<broadcast>" works for most systems. For WAN/NAT, port forwarding is required.
BROADCAST_IP = "<broadcast>"

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
        # Start threads for TCP server, UDP broadcast/listener, and checking peer status.
        threading.Thread(target=self.start_server, daemon=True).start()
        threading.Thread(target=self.udp_broadcast, daemon=True).start()
        threading.Thread(target=self.udp_listener, daemon=True).start()
        threading.Thread(target=self.check_peer_status, daemon=True).start()

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind(("0.0.0.0", self.port))
        except Exception as e:
            print(f"Error binding server on port {self.port}: {e}")
            self.running = False
            return
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
                try:
                    sender_ip_port, sender_team_name, msg = decrypted_message.split(maxsplit=2)
                except ValueError:
                    print("Received malformed message from", addr)
                    continue
                print(f"Received from {sender_ip_port} ({sender_team_name}): {msg}")
                save_message(sender_ip_port, msg)
                # Update peers information (dynamic IP update)
                self.peers[sender_ip_port] = (ip, port)
                save_peers(self.peers)
                # Handle "exit" message: remove peer if requested
                if msg.strip().lower() == "exit":
                    print(f"{sender_ip_port} requested disconnection.")
                    if sender_ip_port in self.peers:
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
            local_ip = socket.gethostbyname(socket.gethostname())
            formatted_message = f"{local_ip}:{self.port} {TEAM_NAME} {message}"
            encrypted_message = encryptor.encrypt(formatted_message.encode())
            client.send(encrypted_message)
            # Update peer info with the latest target details.
            peer_id = f"{target_ip}:{target_port}"
            self.peers[peer_id] = (target_ip, target_port)
            save_peers(self.peers)
            print(f"Message sent to {target_ip}:{target_port}")
        except Exception as e:
            print(f"Failed to connect to {target_ip}:{target_port} - {e}")
        finally:
            client.close()

    def connect_to_peer(self, target_ip, target_port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((target_ip, target_port))
            local_ip = socket.gethostbyname(socket.gethostname())
            connection_message = f"{local_ip}:{self.port} {TEAM_NAME} Connection established"
            encrypted_message = encryptor.encrypt(connection_message.encode())
            client.send(encrypted_message)
            peer_id = f"{target_ip}:{target_port}"
            self.peers[peer_id] = (target_ip, target_port)
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
            try:
                udp_sock.sendto(encryptor.encrypt(message.encode()), (BROADCAST_IP, UDP_PORT))
            except Exception as e:
                print("UDP Broadcast Error:", e)
            time.sleep(5)

    def udp_listener(self):
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            udp_sock.bind(("", UDP_PORT))
        except Exception as e:
            print(f"Error binding UDP listener on port {UDP_PORT}: {e}")
            self.running = False
            return

        discovered_peers = set()  # Track which peers have been printed already
        while self.running:
            try:
                data, addr = udp_sock.recvfrom(1024)
                decrypted = encryptor.decrypt(data).decode()
                peer_info = decrypted.split(":")
                if len(peer_info) != 2:
                    continue
                peer_name, peer_port = peer_info
                peer_ip = addr[0]
                peer_port = int(peer_port)
                peer_id = f"{peer_ip}:{peer_port}"

                # Update dynamic peer information regardless
                self.peers[peer_id] = (peer_ip, peer_port)
                save_peers(self.peers)

                # Only print if the peer has not been discovered before
                if peer_id not in discovered_peers:
                    discovered_peers.add(peer_id)
                    print(f"Discovered peer {peer_name} at {peer_ip}:{peer_port}")
            except Exception as e:
                print("UDP Listener Error:", e)

    def check_peer_status(self):
        while self.running:
            time.sleep(10)
            for peer_id in list(self.peers.keys()):
                ip, port = self.peers[peer_id]
                if not self.is_peer_active(ip, port):
                    print(f"Peer {peer_id} appears offline, removing from list.")
                    del self.peers[peer_id]
                    save_peers(self.peers)

    def is_peer_active(self, ip, port):
        retries = 3
        timeout = 5  # Increase timeout to 5 seconds
        for attempt in range(1, retries + 1):
            try:
                sock = socket.create_connection((ip, port), timeout=timeout)
                sock.close()
                return True
            except Exception as e:
                print(f"Attempt {attempt} to connect to {ip}:{port} failed: {e}")
                time.sleep(1)  # brief pause before retrying
        # After retries, assume the peer is offline.
        return False

    def start(self):
        while self.running:
            print("\n***** Menu *****")
            print("1. Send message")
            print("2. Query active peers")
            print("3. View chat history")
            print("4. Connect to active peer")
            print("0. Quit")
            choice = input("Enter choice: ")
            if choice == "1":
                target_ip = input("Enter recipient's IP: ")
                try:
                    target_port = int(input("Enter recipient's port number: "))
                except ValueError:
                    print("Invalid port number.")
                    continue
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
                try:
                    target_port = int(input("Enter peer's port number: "))
                except ValueError:
                    print("Invalid port number.")
                    continue
                self.connect_to_peer(target_ip, target_port)
            elif choice == "0":
                self.running = False
                break

    def query_active_peers(self):
        print("Connected Peers:")
        if self.peers:
            for peer_id in self.peers:
                print(peer_id, "->", self.peers[peer_id])
        else:
            print("No connected peers.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True, help="Name of the peer")
    parser.add_argument("--port", type=int, required=True, help="Port number for the peer")
    args = parser.parse_args()
    peer = Peer(args.name, args.port)
    peer.start()
