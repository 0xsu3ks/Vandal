import socket,threading,logging,requests,os
from colorama import init, Fore, Style
from prettytable import PrettyTable, ALL
from flask import Flask,app
from .__database import *
from .__utilities import generate_listener_id, is_port_in_use
from vandal_settings import CERT_PATH, KEY_PATH

# The colorama thing
init(autoreset=True)

# Setup logging because sometimes I have no idea what happened
logging.basicConfig(filename='listener.log', level=logging.DEBUG)

# Grab your flask
app = Flask(__name__)

# Lets handle errors in a professional manner
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"An error occurred: {str(e)}", exc_info=True)
    return str(e), 500

class Listener:
    def __init__(self, listener_type, port, secret_key, address='127.0.0.1'):
        self.listener_id = generate_listener_id()
        self.listener_type = listener_type
        self.port = port
        self.secret_key = secret_key
        self.address = address
        
        listener_details = {
            'listener_id': self.listener_id,
            'type': listener_type,
            'port': port,
            'secret_key': secret_key,
            'address': address
        }
        result = active_listeners.insert_one(listener_details)
        print(f"[+] Listener started with ID: {self.listener_id}")

    def start(self):
        if self.listener_type == "local":
            threading.Thread(target=self.start_local_listener).start()
        elif self.listener_type == "HTTP":
            threading.Thread(target=self.start_http_listener).start()

    # This is really not used, for now we will keep it though
    # To test I start a HTTP on local
    def start_local_listener(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', self.port))
            s.listen()
            print(f"Local listener started on port {self.port}")
            while True:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024).decode('utf-8')
                    if data == self.secret_key:
                        print(f"Authenticated connection from {addr}")
                    else:
                        print(f"Failed authentication from {addr}")
    
    # Here is some more madness
    # Every HTTP listener is essentially it's own flask app
    # Flask is very weird when it comes to threading and such, so this was my work around
    def start_http_listener(self):
        logging.basicConfig(filename='debug_log.log', level=logging.DEBUG)
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.DEBUG)
        app.logger.addHandler(logging.FileHandler('debug_log.log'))
        app.logger.setLevel(logging.DEBUG)
        
        os.environ['WERKZEUG_RUN_MAIN'] = 'true'
        # Again values here would be need to be updated to use server args
        app.run(host='0.0.0.0', port=self.port, threaded=True, use_reloader=False)

def stop_http_listener(port):
    try:
        requests.post(f'http://localhost:{port}/shutdown', verify=False)
        print(f"Listener on port {port} stopped successfully!")
        active_listeners.update_one({"port": port}, {"$set": {"state": "inactive"}})

    except Exception as e:
        print(f"Error while stopping listener on port {port}: {e}")

def remove_listener(listener_id):
    # Fetch listener details from the database
    listener = active_listeners.find_one({"listener_id": listener_id})
    
    if not listener:
        print(f"No listener found with ID: {listener_id}")
        return

    # Stop the listener if it's an HTTP listener and it's running
    if listener["type"] == "http":
        stop_http_listener(listener["port"])

    # Remove the listener from the database
    active_listeners.delete_one({"listener_id": listener_id})
    print(f"Listener with ID {listener_id} removed successfully!")


def list_all_listeners():
    all_stored_listeners = list(active_listeners.find({}))
    
    if not all_stored_listeners:
        print("[!] No listeners found")
        return
    
    table = PrettyTable()
    table.field_names = ["ID", "TYPE", "LISTEN-ADDRESS", "PORT", "KEY"]
    for listener in all_stored_listeners:
        table.add_row([Fore.BLUE + Style.BRIGHT + listener["listener_id"] + Fore.RESET, listener["type"], str(listener["address"]), listener["port"], listener["secret_key"]])
    
    table.hrules = ALL
    table.vrules = ALL

    print(table)

def reactivate_stored_listeners():
    # This was a big problem but eventually, I just thought to delete the listener and recreate it
    # That's what this does
    client = MongoClient('localhost', 27017)
    db = client['vandal_db']
    active_listeners = db['listeners']

    all_stored_listeners = list(active_listeners.find({}))
    
    for listener_details in all_stored_listeners:
        
        active_listeners.delete_one({"listener_id": listener_details["listener_id"]})
        
        listener = Listener(listener_details['type'], listener_details['port'], listener_details['secret_key'])
        listener.start()
        #print(f"Recreated and started {listener_details['type']} listener on port {listener_details['port']}")

def listener_types():
    table = PrettyTable()
    table.field_names = ["Type", "Purpose"]
    table.add_row(["HTTP", "Channel communications over HTTP(s)"])
    
    table.hrules = ALL
    table.vrules = ALL

    print(table)
