from colorama import Fore, init, Style
import shutil




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

intro_art()

print('\nVANDAL C2 Configuration Setup\n')
print('Leave blank for default')

input_secret_key = input("Enter the server secret key [default: PASSWORD]: ").strip()
SECRET_KEY = input_secret_key if input_secret_key else "PASSWORD"

try:
    input_port = int(input("Enter the port to run the Vandal server [default: 22885]: ").strip())
    PORT = input_port if input_port else 22885
except ValueError:
    print("Invalid port. Setting to default: 22885.")
    PORT = 22885

input_cert_path = input("Enter the path to your SSL certificate: ").strip()
CERT_PATH = input_cert_path if input_cert_path else "./cert.pem"

input_key_path = input("Enter the path to your SSL private key: ").strip()
KEY_PATH = input_key_path if input_key_path else "./key.pem"

input_mongo_address = input("Enter address for MongoDB [default http://127.0.0.1]: ")
MONGO_PATH = input_mongo_address if input_mongo_address else "127.0.0.1"

input_mongo_port = input("Enter port for MongoDB [default: 27017]: ")
MONGO_PORT = int(input_mongo_port) if input_mongo_port else 27017


with open("vandal_settings.py", "w") as config_file:
    config_file.write("# CHANGING ANYTHING HERE MAY BREAK THE APPLICATION\n")
    config_file.write("# IF CHANGES NEED TO BE MADE RERUN THE CONFIGURATION SCRIPT\n\n")
    config_file.write(f"SECRET_KEY = '{SECRET_KEY}'\n")
    config_file.write(f"PORT = {PORT}\n")
    config_file.write(f"CERT_PATH = '{CERT_PATH}'\n")
    config_file.write(f"KEY_PATH = '{KEY_PATH}'\n")
    config_file.write(f"MONGO_PATH = '{MONGO_PATH}'\n")
    config_file.write(f"MONGO_PORT = {MONGO_PORT}\n")

print(Fore.CYAN + "[+]Configuration set!" + Fore.RESET)

source = "vandal_settings.py"
destination = "utils/db/vandal_settings.py"
shutil.copy(source, destination)