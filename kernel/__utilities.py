import random,string,socket
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

