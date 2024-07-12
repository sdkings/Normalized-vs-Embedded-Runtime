import json
import time
import sys
from pymongo import MongoClient
from pymongo.errors import BulkWriteError, PyMongoError

# Function to read JSON file as an array
def read_json_array(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            for item in data:
                yield item
    except FileNotFoundError as e:
        print(f'Error: {e}')
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        sys.exit(1)

# Function to insert data into MongoDB in batches
def insert_in_batches(collection, data_generator, batch_size=5000):
    batch = []
    try:
        for document in data_generator:
            batch.append(document)
            if len(batch) == batch_size:
                collection.insert_many(batch)
                batch = []
        if batch:  # Insert any remaining messages
            collection.insert_many(batch)
    except BulkWriteError as e:
        print(f"Error during batch insertion: {e.details}")
    except PyMongoError as e:
        print(f"MongoDB error: {e}")
        sys.exit(1)

# Function to create 'messages' collection
def create_messages_collection(db):
    print("Creating 'messages' collection...")
    messages_collection = db['messages']
    messages_collection.drop()  # Drop collection if exists
    start_time = time.time()
    insert_in_batches(messages_collection, read_json_array('messages.json'))
    end_time = time.time()
    print(f"Time taken to create 'messages' collection: {end_time - start_time:.2f} seconds")

# Function to create 'senders' collection
def create_senders_collection(db):
    print("Creating 'senders' collection...")
    senders_collection = db['senders']
    senders_collection.drop()  # Drop collection if exists
    start_time = time.time()
    try:
        with open('senders.json', 'r') as file:
            senders_data = json.load(file)
            senders_collection.insert_many(senders_data)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except PyMongoError as e:
        print(f"MongoDB error: {e}")
        sys.exit(1)
    end_time = time.time()
    print(f"Time taken to create 'senders' collection: {end_time - start_time:.2f} seconds")

def main():
    if len(sys.argv) != 2:
        print("Usage: python task1_build.py <port_number>")
        return

    port_number = int(sys.argv[1])

    try:
        # Connect to MongoDB
        client = MongoClient('localhost', port_number)
        print("Connected to MongoDB.")

        # Create or get the MP2Norm database
        db = client['MP2Norm']

        # Step 1: Create 'messages' collection
        create_messages_collection(db)

        # Step 2: Create 'senders' collection
        create_senders_collection(db)

        print("Database creation and data insertion completed successfully.")
    except PyMongoError as e:
        print(f"Error connecting to MongoDB: {e}")
    finally:
        if 'client' in locals():
            client.close()
            print("MongoDB connection closed.")

if __name__ == "__main__":
    main()
