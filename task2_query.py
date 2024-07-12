import sys
import time
from pymongo import MongoClient, errors

def execute_query_with_timing(db, query_function, query_description):
    try:
        start_time = time.time()
        result = query_function(db)
        end_time = time.time()
        print(f"{query_description} Result: {result}, Time taken: {(end_time - start_time) * 1000:.2f} milliseconds")
    except errors.ExecutionTimeout:
        print(f"{query_description} Query takes more than two minutes.")

def execute_update_with_timing(db, update_function, update_description):
    try:
        start_time = time.time()
        update_function(db)
        end_time = time.time()
        print(f"{update_description} Time taken: {(end_time - start_time) * 1000:.2f} milliseconds")
    except errors.ExecutionTimeout:
        print(f"{update_description} Query takes more than two minutes.")

def query1(db):
    """Return the number of messages that have 'ant' in their text (case-sensitive)."""
    return db.messages.count_documents({"text": {"$regex": "ant"}}, maxTimeMS=120000)  

def query2(db):
    """Find the sender with the greatest number of messages."""
    pipeline = [
        {"$group": {"_id": "$sender", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ]
    result = list(db.messages.aggregate(pipeline, maxTimeMS=120000))
    if result:
        return f"Sender: {result[0]['_id']}, Messages: {result[0]['count']}"
    else:
        return "No data found."

def query3(db):
    """Count messages where sender's credit is 0."""
    return db.messages.count_documents({"sender_info.credit": 0}, maxTimeMS=120000)

def query4(db):
    """Double the credit of all senders whose credit is less than 100."""
    try:
        db.messages.update_many(
            {"sender_info.credit": {"$lt": 100}},
            {"$mul": {"sender_info.credit": 2}},
        )
    except errors.ExecutionTimeout:
        print("Query takes more than two minutes.")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_indices(db):
    """Create indices for 'text', 'sender', and 'sender_info.credit' fields."""
    print("Creating indices...")
    db.messages.create_index([("text", "text")])
    db.messages.create_index([("sender", 1)])
    db.messages.create_index([("sender_info.credit", 1)])
    print("Indices creation completed.")

def execute_queries_1_to_3(db):
    execute_query_with_timing(db, query1, "Q1: Count messages containing 'ant'")
    execute_query_with_timing(db, query2, "Q2: Sender with the greatest number of messages")
    execute_query_with_timing(db, query3, "Q3: Count messages where sender's credit is 0")

def main(port_number):
    client = MongoClient('localhost', port_number)
    db = client.MP2Embd

    print("Executing queries 1, 2, and 3 before creating indices:")
    execute_queries_1_to_3(db)

    # Create Indices
    create_indices(db)

    print("\nRe-executing queries 1, 2, and 3 after creating indices to observe performance changes:")
    execute_queries_1_to_3(db)

    print("\nExecuting query 4 to double credits for senders with credit less than 100:")
    execute_update_with_timing(db, query4, "Q4: Double the credit for senders with credit less than 100")

    client.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <port_number>")
        sys.exit(1)
    
    port_number = int(sys.argv[1])
    main(port_number)
