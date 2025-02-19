# p2p_chat
Blockchain project to implement p2p chat system
terminal 1 output
(.venv) PS C:\Users\harsh\PyCharm_Project\p2p_chat> python chat.py --name Peer1 --port 8080
Server listening on port 8080...

***** Menu *****
1. Send message
2. Query active peers
3. View chat history
4. Connect to active peers
0. Quit
Enter choice: Discovered peer Peer1 at 10.18.3.172:8080
Discovered peer Peer2 at 10.18.3.172:9090
Discovered peer Peer3 at 10.18.3.172:7070
1
Enter recipient's IP: 127.0.0.1
Enter recipient's port number: 9090
Enter your message: Hello Peer2
Message sent to 127.0.0.1:9090

***** Menu *****
1. Send message
2. Query active peers
3. View chat history
4. Connect to active peers
0. Quit
Enter choice: 4
Enter peer's IP: 127.0.0.1
Enter peer's port number: 7070
Connected to 127.0.0.1:7070

***** Menu *****
1. Send message
2. Query active peers
3. View chat history
4. Connect to active peers
0. Quit
Enter choice:

terminal 2
(.venv) PS C:\Users\harsh\PyCharm_Project\p2p_chat> python chat.py --name Peer2 --port 9090
Server listening on port 9090...

***** Menu *****
1. Send message
2. Query active peers
3. View chat history
4. Connect to active peers
0. Quit
Enter choice: Discovered peer Peer2 at 10.18.3.172:9090
Discovered peer Peer3 at 10.18.3.172:7070
10.18.3.172:8080 CryptoCrafters Hello Peer2
2
Connected Peers:
10.18.3.172:8080
10.18.3.172:9090
10.18.3.172:7070

***** Menu *****
1. Send message
2. Query active peers
3. View chat history
4. Connect to active peers
Enter choice: 3
(1, '10.18.3.172:8080', 'Hello Peer2', 'Wed Feb 19 02:21:59 2025')

***** Menu *****
1. Send message
2. Query active peers
3. View chat history
4. Connect to active peers
0. Quit
Enter choice:

terminal 3
(.venv) PS C:\Users\harsh\PyCharm_Project\p2p_chat> python chat.py --name Peer3 --port 7070
Server listening on port 7070...

** Menu **
1. Send message
2. Query active peers
3. View chat history
4. Connect to active peers
0. Quit
Enter choice: Discovered peer Peer3 at 10.18.3.172:7070
10.18.3.172:8080 CryptoCrafters Connection established
