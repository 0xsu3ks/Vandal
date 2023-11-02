from vandal_settings import MONGO_PATH,MONGO_PORT
from pymongo import MongoClient
from colorama import Fore, init

# Connect to MongoDB
client = MongoClient(MONGO_PATH, MONGO_PORT)

# Select the database and collection
db = client['vandal_db']
listeners = db['listeners']
agents = db['agents']
jobs = db['jobs']

listeners.delete_many({})
agents.delete_many({})
jobs.delete_many({})
print(Fore.CYAN + "[+]All items from 'listeners' collection have been deleted.")
print("[+]All documents from 'agents' collection have been deleted.")
print("[+]All documents from 'jobs' collection have been deleted." + Fore.RESET)
