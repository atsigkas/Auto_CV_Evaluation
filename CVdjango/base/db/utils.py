from pymongo import MongoClient, errors, TEXT
import json


class MongoDBHandler:
    def __init__(self, domain, port):
        self.domain = domain
        self.port = port
        self.client = None
        self.connection_string = f"{self.domain}:{self.port}"

    def connect(self):
        try:
            self.client = MongoClient(host=[self.connection_string], serverSelectionTimeoutMS=2000)
            print(f"Trying to connect to MongoDB server: {self.connection_string}")
            print("server_info():", self.client.server_info())
        except errors.ServerSelectionTimeoutError as err:
            print(f"pymongo ERROR: {err}")
            self.client = None
        return self.client

    def get_database_and_collection(self, db_name, collection_name):
        try:
            if self.client:
                db = self.client[db_name]
                col = db[collection_name]
                return db, col
            else:
                raise AttributeError("Client instance is invalid.")
        except AttributeError as error:
            print(f"Get MongoDB database and collection ERROR: {error}")
            return None, None

    def find_document(self, collection, candidate):
        try:
            return collection.find(
                {
                    "$or": [
                        {"author": candidate["author"]},
                        {"email": candidate["email"]},
                        {"phone": candidate["phone"]}
                    ]
                }
            )
        except errors.ServerSelectionTimeoutError as err:
            print(f"Find_one() ERROR: {err}")
            return None

    def find_document_one(self, collection,var, name):
        try:
            return collection.find_one({var: name})
        except errors.ServerSelectionTimeoutError as err:
            print(f"Find_one() ERROR: {err}")
            return None
    def insert_one_document(self, collection,candidate):
        try:
            return collection.insert_one(candidate)
        except errors.ServerSelectionTimeoutError as err:
            print(f"Insert_one() ERROR: {err}")
            return None

    def close(self):
        try:
            if self.client:
                self.client.close()
                print(f"Connection to MongoDB server: {self.connection_string} has been closed.")
            else:
                print("No active connection found.")
        except Exception as error:
            print(f"Error occurred while trying to close the connection: {error}")
