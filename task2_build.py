import json
import sys
import time
from pymongo import MongoClient
from pymongo.errors import BulkWriteError, ConnectionFailure

# Function to read JSON file as an array
def read_json_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(f"Error: The file {filename} was not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {filename}: {e}")
        sys.exit(1)

# Function to insert data into MongoDB in batches
def insert_in_batches(collection, data, batch_size=5000):
    try:
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            collection.insert_many(batch)
    except BulkWriteError as e:
        print(f"Error during batch insertion: {e.details}")
        sys.exit(1)

# Main function to create 'messages' collection with embedded 'senders' info
def main(port_number):
    try:
        # Connect to MongoDB
        client = MongoClient('localhost', port_number, serverSelectionTimeoutMS=5000)
        client.server_info()  # Force connection on a request as the MongoClient's connect is lazy.
        print("Connected to MongoDB.")
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
        sys.exit(1)

    db = client['MP2Embd']
    # Drop the 'messages' collection if it exists
    db.messages.drop()

    # Load 'senders' information into memory
    senders_info = read_json_file('senders.json')
    # Create a dictionary for faster lookup
    senders_dict = {sender['sender_id']: sender for sender in senders_info}

    # Prepare 'messages' data with embedded 'sender_info'
    messages = read_json_file('messages.json')
    for message in messages:
        # Check if sender exists in senders_dict and embed sender_info
        sender_info = senders_dict.get(message['sender'])
        if sender_info:
            message['sender_info'] = sender_info
        else:
            print(f"Warning: Sender {message['sender']} not found in senders.json.")

    # Record the start time
    start_time = time.time()

    # Insert messages into the 'messages' collection in batches
    insert_in_batches(db.messages, messages)

    # Record the end time and print the time taken to insert the data
    end_time = time.time()
    print(f"Time taken to create 'messages' collection: {end_time - start_time:.2f} seconds")

    # Close MongoDB connection
    client.close()
    print("MongoDB connection closed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python task2_build.py <port_number>")
        sys.exit(1)
    
    port_number = int(sys.argv[1])
    main(port_number)
