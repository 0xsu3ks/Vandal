#THIS IS NOT CURRENTLY BEING USED, LEAVING HERE FOR REFERENCE


from flask import Flask, jsonify
from vandal_settings import PORT
#from gevent.pywsgi import WSGIServer
import threading
import socket


import socketserver
import socks

# A global dictionary to keep track of running proxy instances per agent
proxy_servers = {}

class ThreadingSOCKSServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class SocksProxy(socketserver.StreamRequestHandler):
    def __init__(self, request, client_address, server, agent_address):
        self.agent_address = agent_address
        super().__init__(request, client_address, server)

    def handle(self):
        agent_full_address = (self.agent_address, PORT)
        try:
            # Initialize a connection to the agent
            agent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            agent_socket.connect(agent_full_address)
            
            while True:
                # Receive data from the client (e.g., your machine using proxychains)
                data = self.request.recv(8192)
                if not data:
                    break
                
                # Send the data to the agent
                agent_socket.send(data)
                
                # Receive a response from the agent
                received = agent_socket.recv(8192)
                if not received:
                    break
                
                # Send the agent's response back to the client
                self.request.send(received)
                
        except Exception as e:
            print(f"SOCKS error: {e}")
        finally:
            agent_socket.close()

# A global dictionary to keep track of running proxy instances per agent



# app = Flask(__name__)

# @app.route('/command', methods=['GET'])
# def send_command():
#     # Dummy command for demonstration
#     return jsonify({"command": "collect_system_info"})

# @app.route('/collect', methods=['POST'])
# def collect_data():
#     # Placeholder for collecting data from compromised host
#     return jsonify({"status": "data_received"})

# def start_socks_proxy():
#     # Placeholder for the SOCKS proxy logic
#     # This will handle incoming SOCKS requests and route them appropriately
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind(('0.0.0.0', 1080))
#         s.listen()
#         conn, addr = s.accept()
#         # Handle the connection here...
#         # You can integrate the SOCKS logic you provided earlier
#         # Remember to loop and handle multiple clients

# if __name__ == "__main__":
#     # Start the SOCKS proxy in a separate thread
#     threading.Thread(target=start_socks_proxy).start()
    
#     # Start the Flask C2 server using gevent
#     http_server = WSGIServer(('0.0.0.0', 5000), app)
#     http_server.serve_forever()




#TCP FORWARD
# class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
#     def handle(self):
#         cur_thread = threading.current_thread()
#         print(f"[+] Received connection on {cur_thread.name}")

#         # Connect to the target
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as target_sock:
#             try:
#                 target_sock.connect((TARGET_IP, TARGET_PORT))
#             except Exception as e:
#                 print(f"[-] Failed to connect to {TARGET_IP}:{TARGET_PORT}")
#                 return

#             # Start a thread to receive data from the target and send it to the source
#             def target_to_source(source, target):
#                 while True:
#                     data = target.recv(4096)
#                     if not data:
#                         break
#                     source.sendall(data)

#             t = threading.Thread(target=target_to_source, args=(self.request, target_sock))
#             t.start()

#             # Read data from source and forward to target
#             while True:
#                 data = self.request.recv(4096)
#                 if not data:
#                     break
#                 target_sock.sendall(data)

#         print(f"[-] Connection closed on {cur_thread.name}")

# class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
#     pass

# if __name__ == "__main__":
#     # Define the target IP and port to which you want to forward the traffic
#     TARGET_IP = '192.168.1.100'  # Modify this to the desired IP
#     TARGET_PORT = 80  # Modify this to the desired port

#     # Start the TCP server
#     server_ip = '0.0.0.0'  # Listen on all interfaces
#     server_port = 9999  # Port on which the server will listen for incoming connections
#     server = ThreadedTCPServer((server_ip, server_port), ThreadedTCPRequestHandler)
#     with server:
#         ip, port = server.server_address
#         print(f"[*] Listening on {ip}:{port}")
#         server_thread = threading.Thread(target=server.serve_forever)
#         server_thread.start()
