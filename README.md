[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/Fozs_Okj)
# CMPUT 291 Mini Project 2 - Winter 2024  
Group member names and ccids (3-4 members)  
  sapandee, Sapandeep Singh
  harveers, Harveer Singh Sarao   
  damansin, Daman Singh Batra
  bakhshis, Bakhshish Sethi

# Group work break-down strategy
Sapandeep led the group, managed tasks, and ensured timely completion. Bakshish implemented task1_build, focusing on data handling and MongoDB collection creation. Harveer handled task2_build, emphasizing data processing and embedding sender information. Sapandeep wrote task1_query, optimizing MongoDB queries and error handling. Daman completed task2_query, analyzing query performance and model suitability. Regular updates and collaboration ensured successful task completion within the deadline.

# Code execution guide
1. Make sure your environment has mongdb and pymongo installed.
2. Make sure all the files are in the same directory.
3. Set up a MongoDb connection in the same diectory and note down the port number.
4. On the terminal, write python3 task1_build.py port number in order to build the normalized datastore.(Replace port number by the actual 5 digit port number you used to establish mongodb connection)
5. After creating the normalized datastore,write python3 task1_query.py port number in order to run the queries.
6. On the terminal, write python3 task2_build.py port number in order to build the embedded datastore.(Replace port number by the actual 5 digit port number you used to establish mongodb connection)
7. After creating the embedded datastore,write python3 task2_query.py port number in order to run the queries.


# AI Agents
Yes, we have used the AI agent ChatGPT, https://chat.openai.com/

The problem with ChatGPT is that if you provide it with the question straight-up, it gives a faulty response that is mostly always incorrect. So our group made sure that we only asked doubts, and used the AI model to learn concepts using examples. Below I will be sharing the prompts that our group gave ChatGPT, which will be followed by the AI model's response and a brief description of what we learned and how we used it. 

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Prompt 1) We are given with two tasks for our project. First, building a normalized document store, and second, building an embedded document store. Both tasks need to be accomplished using MongoDB and Python. Any advice on how to go about it?

ChatGPT's Response: 

To achieve the tasks you've outlined, we'll break down the process into structured steps for both Task 1 (building a normalized document store) and Task 2 (building an embedded document store). This will guide you through programming, database operations, and performance analysis in MongoDB, focusing on data modeling, indexing, and querying.
Setting Up MongoDB Connection: Use pymongo to connect to your MongoDB instance running on the given port. Make sure MongoDB is installed and running.
Creating the Database: Instantiate a database called MP2Norm.
Handling Large JSON Files: For messages.json, use a streaming JSON parser like ijson to process the file without loading it entirely into memory. This allows you to read and insert data in batches.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

Prompt 2) Can you give us tips to handle large json files? Implemented using Python and MongoDB. 

ChatGPT's Response:

Handling large JSON files in this project can be challenging due to memory constraints and performance considerations. Here are some tips to handle large JSON files effectively:
Use Streaming: Instead of loading the entire JSON file into memory at once, consider streaming the data. Python's json module supports streaming with functions like json.load() and json.loads(). This way, you can process the data in chunks, reducing memory usage.
Batch Processing: Break down the JSON file into smaller batches and process each batch separately. This can help manage memory usage and prevent performance issues. You can implement batch processing using loops and iterators
Compress JSON Files: If the JSON files are too large, consider compressing them using tools like gzip or bz2. This can reduce the file size and make it easier to handle, especially during transfer or storage.
Use Disk-based Storage: If the JSON files are too large to fit into memory, consider using disk-based storage solutions such as databases or file-based databases like SQLite. These solutions allow you to query and process large datasets efficiently without loading everything into memory.

By following these tips, you can effectively handle large JSON files in your project while ensuring optimal performance and resource utilization.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Prompt 3) What are the steps involved in making an embedded document store? How is it different from the normalized one?

ChatGPT's Response:

Building an Embedded Document Store
Step 1: Writing task2_build.py
Preparation: Load senders.json into memory using an appropriate data structure, mapping sender_id to sender details.
Embedding Sender Info: Process messages.json similarly to Task 1, but for each message, enrich it with the corresponding sender_info from your in-memory data before inserting into the database.
Database Operations: Similar to Task 1, measure and report the time taken to complete the database operations.
Step 2: Queries and Performance Analysis
Re-implementing Queries: Execute the same queries as in Task 1, adapted for the embedded document structure.

Performance Comparison: Analyze and compare the performance of each query in the normalized versus embedded model, providing insights on data retrieval efficiency, and explain why one model may be preferable over the other for specific queries.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Collaborations
Did not collorabate with anyone else. 
