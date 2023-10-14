from pymongo import MongoClient

def insert_dummy_record(collection):
    # Insert a dummy listener
    listener_details = {
        'type': 'test',
        'port': 12345,
        'secret_key': 'test_key'
    }
    collection.insert_one(listener_details)
    print("Inserted dummy record.")

def fetch_and_print_records(collection):
    # Fetch and print all listeners
    all_listeners = list(collection.find({}, {'_id': False}))
    print("Current records:", all_listeners)

def clear_collection(collection):
    # Delete all documents from the collection
    collection.delete_many({})
    print("All documents have been deleted.")

def main():
    # Connect to MongoDB
    client = MongoClient('localhost', 27017)

    # Select the database and collection
    db = client['listener_db']
    collection = db['listeners']

    insert_dummy_record(collection)
    fetch_and_print_records(collection)

    # Clear collection
    clear_collection(collection)
    fetch_and_print_records(collection)

if __name__ == "__main__":
    main()
