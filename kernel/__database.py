from vandal_settings import MONGO_PATH,MONGO_PORT
from pymongo import MongoClient

client = MongoClient(MONGO_PATH, MONGO_PORT)
db = client['vandal_db']
active_listeners = db['listeners']
active_agents = db['agents']
jobs_collection = db['jobs']
beats_collection = db['heartbeats']