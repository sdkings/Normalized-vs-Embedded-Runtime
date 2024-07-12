import sys
import time
from pymongo import MongoClient, errors

def execute_query_with_timing(db, query_function):
    try:
        start_time = time.time()
        result = query_function(db)
        end_time = time.time()
        print(f"Result: {result}, Time taken: {(end_time - start_time) * 1000:.2f} milliseconds")
    except errors.ExecutionTimeout:
        print("Query takes more than two minutes.")
    except errors.PyMongoError as e:
        print(f"MongoDB error during query execution: {e}")

def execute_update_with_timing_only(db, update_function, update_description):
    try:
        start_time = time.time()
        update_function(db)  # The result of the update operation is not used.
        end_time = time.time()
        print(f"{update_description} Time taken: {(end_time - start_time) * 1000:.2f} milliseconds")
    except errors.ExecutionTimeout:
        print(f"{update_description} Query takes more than two minutes.")
    except errors.PyMongoError as e:
        print(f"MongoDB error during update operation: {e}")        

# Queries
def query1(db):
    """Return the number of messages that have 'ant' in their text (case-sensitive)."""
    try:
        return db.messages.count_documents({'text': {'$regex': 'ant'}}, maxTimeMS=120000)
    except errors.ExecutionTimeout:
        return "Query takes more than two minutes."

def query2(db):
    """Find the sender who has sent the greatest number of messages."""
    try:
        pipeline = [
            {'$group': {'_id': '$sender', 'total_messages': {'$sum': 1}}},
            {'$sort': {'total_messages': -1}},
            {'$limit': 1}
        ]
        result = list(db.messages.aggregate(pipeline, maxTimeMS=120000))
        if result:
            return f"Sender: {result[0]['_id']}, Messages: {result[0]['total_messages']}"
        else:
            return "No data found."
    except errors.ExecutionTimeout:
        return "Query takes more than two minutes."

def query3(db):
    """Return the number of messages where the sender's credit is 0."""
    try:
        sender_ids = db.senders.find({'credit': 0}, {'sender_id': 1})
        sender_ids = [sender['sender_id'] for sender in sender_ids]
        
        pipeline = [
            {'$match': {'sender': {'$in': sender_ids}}},
            {'$count': 'zero_credit_messages'}
        ]
        
        result = list(db.messages.aggregate(pipeline, maxTimeMS=120000))
        return result[0]['zero_credit_messages'] if result else 0
    except errors.ExecutionTimeout:
        return "Query takes more than two minutes."

    
def query4(db):
    """Double the credit of all senders whose credit is less than 100. Only execution time is printed."""
    db.senders.update_many(
        {'credit': {'$lt': 100}},
        {'$mul': {'credit': 2}},
    )

def create_indices(db):
    """Create indices for the 'messages' and 'senders' collections."""
    print("Creating indices...")
    db.messages.create_index([('sender', 1)])
    db.messages.create_index([('text', 'text')])
    db.senders.create_index([('sender_id', 1)])

def main(port_number):
    client = MongoClient('localhost', port_number)
    db = client['MP2Norm']

    try:
        # Execute queries before indexing
        print("Executing Query 1 (before indexing):")
        execute_query_with_timing(db, query1)

        print("Executing Query 2 (before indexing):")
        execute_query_with_timing(db, query2)

        print("Executing Query 3 (before indexing):")
        execute_query_with_timing(db, query3)

        # Creating indices
        create_indices(db)

        # Repeat queries after creating indices
        print("\nAfter creating indices, re-executing Query 1:")
        execute_query_with_timing(db, query1)

        print("After creating indices, re-executing Query 2:")
        execute_query_with_timing(db, query2)

        print("After creating indices, re-executing Query 3:")
        execute_query_with_timing(db, query3)

        # Executing Query 4 with only runtime information
        print("Executing Query 4 to double credits for senders with credit less than 100:")
        execute_update_with_timing_only(db, query4, "Query 4 - Double credit for senders")
    finally:
        client.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <port_number>")
        sys.exit(1)

    port_number = int(sys.argv[1])
    main(port_number)
