from pprint import pprint
import certifi as certifi
import pymongo as pym
from pymongo import errors

client = None

MOCK_DATA = [
    {
        'name': 'Peter Parker',
        'ssn': '000.00.0000',
        'address': '123 Main St, Anytown',
        'accounts': [
            {
                'agency': '0001',
                'number': 1234,
                'balance': 1000,
            },
        ],
    },
    {
        'name': 'Mary Jane Watson',
        'ssn': '000.00.0001',
        'address': '321 Elm St, Another Town',
        'accounts': [
            {
                'agency': '0001',
                'number': 9999,
            },
            {
                'type': 'Savings',
                'agency': '0001',
                'number': 51009999,
                'balance': 300.00,
            },
        ],
    },
    {
        'name': 'Gwen Stacy',
        'ssn': '000.00.0002',
        'address': '999 Oak St, Inverted World',
        'accounts': [
            {
                'agency': '0001',
                'number': 4321,
                'balance': 30,
            },
        ],
    }
]

USERNAME = 'mongodbbrendafazeredo'
PASSWORD = 'ffRJsesKnjSJlyQO'
MONGODB_CLUSTER_URI = 'cluster11.3fidigc.mongodb.net'
DATABASE = 'my_database'

MONGO_DB_URI = f'mongodb+srv://{USERNAME}:{PASSWORD}@{MONGODB_CLUSTER_URI}/{DATABASE}?retryWrites=true&w=majority'

try:
    client = pym.MongoClient(MONGO_DB_URI, tlsCAFile=certifi.where())
    db = client.get_database(DATABASE)

    if client is not None and db is not None:
        print(f"Connected to database: {db.name}")

        clients = db["clients"]
        client_ids = clients.insert_many(MOCK_DATA)
        print(f"Inserted client IDs: {client_ids.inserted_ids}")

        print(f"Collection names in the database: {db.list_collection_names()}")

        pprint(clients.find_one({'name': 'Mary Jane Watson'}))
        for item in clients.find():
            pprint(item)

        count_result = clients.count_documents({'ssn': '000.00.0000'})
        print(f"Count of clients with SSN '000.00.0000': {count_result}")
    else:
        print("Failed to establish a connection to MongoDB.")

except errors.PyMongoError as e:  # Use 'errors' from pymongo
    print(f"MongoDB Error: {str(e)}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    if client is not None:
        client.close()
