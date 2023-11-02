import random,string,socket,os,subprocess
from colorama import Fore,init,Style
from bson import ObjectId
from .__database import *

def generate_listener_id(length=6):
    characters = string.ascii_letters + string.digits 
    return ''.join(random.choice(characters) for _ in range(length))

def generate_agent_id(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        agent_id = ''.join(random.choice(characters) for _ in range(length))
        # Check if the generated ID already exists in the database
        if not active_agents.find_one({"agent_id": agent_id}):
            return agent_id
        
def json_serial(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError("Type not serializable")

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("0.0.0.0", port))
            return False
        except socket.error:
            return True  

def intro_art():
    print(Fore.BLUE + Style.BRIGHT + ".·:''''''''''''''''''''''''''''''''''''''''''''':·.")
    print(Fore.BLUE + Style.BRIGHT + ": :                                             : :")
    print(Fore.BLUE + Style.BRIGHT + ": :                                             : :")
    print(Fore.BLUE + Style.BRIGHT + ": :                                             : :")
    print(Fore.BLUE + Style.BRIGHT + ": :   __     ___    _   _ ____    _    _        : :")
    print(Fore.BLUE + Style.BRIGHT + ": :   \ \   / / \  | \ | |  _ \  / \  | |       : :")
    print(Fore.WHITE + Style.BRIGHT + ": :    \ \ / / _ \ |  \| | | | |/ _ \ | |       : :")
    print(Fore.WHITE + Style.BRIGHT + ": :     \ V / ___ \| |\  | |_| / ___ \| |___    : :")
    print(Fore.RED + Style.BRIGHT + ": :      \_/_/   \_\_| \_|____/_/   \_\_____|   : :")
    print(Fore.RED + Style.BRIGHT + ": :                                        " + Fore.RESET + Fore.BLUE + Style.BRIGHT + "C2" + Fore.RESET + Fore.RED +  "   : :")
    print(Fore.RED + Style.BRIGHT + ": :                                   " + Fore.RESET + Fore.WHITE + Style.BRIGHT + "0xsu3ks" + Fore.RESET + Fore.RED +  "   : :")
    print(Fore.RED + Style.BRIGHT + ": :                                      " + Fore.RESET + Fore.RED + Style.BRIGHT + "v0.1" + Fore.RESET + Fore.RED + "   : :")
    print(Fore.RED + Style.BRIGHT + ": :                                             : :")
    print(Fore.RED + Style.BRIGHT + "'·:.............................................:·'" + Fore.RESET)

def generate_exe(script_name):
    command = f'./myvenv/bin/pyinstaller --onefile --windowed {script_name}'  # Use the PyInstaller from virtual env
    with open(os.devnull, 'w') as fnull:
        subprocess.run(command, stdout=fnull, stderr=fnull, shell=True)

def create_venv_and_run_pyinstaller(script_name):
    # Step 1: Create a virtual environment named 'myvenv' in the current directory
    print("[+] Building virtual enviornment...")
    with open(os.devnull, 'w') as fnull:
        subprocess.run(["python3", "-m", "venv", "myvenv"], stdout=fnull, stderr=fnull)

    # Depending on the OS, the activation script location differs
    print("Checking OS...")
    if os.name == 'posix':  # For Linux and macOS
        print("[!] Linux")
        activate_script = './myvenv/bin/activate'
    elif os.name == 'nt':  # For Windows
        print("[!] Windows")
        activate_script = '.\\myvenv\\Scripts\\activate.bat'
    else:
        raise ValueError("Unknown OS")

    # Step 2: Install pyinstaller within the virtual environment
    with open(os.devnull, 'w') as fnull:
        subprocess.run(f"source {activate_script} && pip install pyinstaller", stdout=fnull, stderr=fnull, shell=True, executable="/bin/bash")

    # Step 3: Run your existing function
    print("[+] Building executable")
    generate_exe(script_name)
    print("[+] Executable saved to dist/ directory")

# import socket
# import socks  # Ensure you have PySocks installed

# def start_socks_proxy(listen_ip, listen_port):
#     # This starts a SOCKS proxy on the specified IP and port.
#     socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, listen_ip, listen_port)
#     socket.socket = socks.socksocket  # All socket communications now use the SOCKS proxy
    
#     # Keep the proxy running
#     while True:
#         pass

# start_socks_proxy('0.0.0.0', 1080)  # Start SOCKS proxy on all interfaces, port 1080

#FlASK GEVENT

commands_queue = {}

def enqueue_command_for_agent(agent_id, command):
    """
    Add a command to the queue for a specific agent.

    Args:
    - agent_id (str): The ID of the agent.
    - command (str): The command to be executed by the agent.

    Returns:
    - None
    """
    if agent_id not in commands_queue:
        commands_queue[agent_id] = []

    commands_queue[agent_id].append(command)


def get_agent_address(agent_id):
    # Connect to the MongoDB server
    client = MongoClient('localhost', 27017)

    # Select your database and collection
    db = client['vandal_db']
    agents = db['agents']

    # Find the agent by agent_id
    agent = agents.find_one({'agent_id': agent_id})

    # Close the connection
    client.close()

    if agent:
        return agent["ip_address"]
    else:
        raise ValueError(f"No agent found with ID: {agent_id}")