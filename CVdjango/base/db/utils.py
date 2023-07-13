from pymongo import MongoClient, errors, TEXT


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

    def find_document(self, collection, name):
        try:
            return collection.find({"Author": name})
        except errors.ServerSelectionTimeoutError as err:
            print(f"Find_one() ERROR: {err}")
            return None

    def insert_one_document(self, collection):
        try:
            candidate = {
                "Author": "Stavros Solakis",
                "title": "Neural Networks",
                "email": "ssolakis@email.com",
                "phone": "53453545345",
                "Publications": [{
                    "title": "Comparative Analysis of Machine Algorithms for Sentiment Analysis",
                    "year": "1995"
                    }, {
                    "title": "pame",
                    "year": "1995"
                }]
            }
            return collection.insert_one(candidate)
        except errors.ServerSelectionTimeoutError as err:
            print(f"Insert_one() ERROR: {err}")
            return None
