from pymongo import MongoClient, errors
from bson.objectid import ObjectId
import logging
import pandas as pd

logging.basicConfig(level=logging.ERROR)

class AnimalShelter:
    def __init__(self, user, password, host, port, db, col):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db = db
        self.col = col
        try:
            self.client = MongoClient(f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}')
            self.database = self.client[self.db]
            self.collection = self.database[self.col]
            print("Connected successfully to MongoDB")
        except errors.ConnectionFailure as e:
            logging.error(f"Could not connect to MongoDB: {e}")
            self.client = None
            self.database = None
            self.collection = None

    def close(self):
        if self.client:
            self.client.close()

    def create(self, data):
        if self.collection is None:
            logging.error("Database connection is not established. Cannot perform create operation.")
            return False

        if data is not None:
            try:
                result = self.collection.insert_one(data)
                return result.inserted_id
            except errors.PyMongoError as e:
                logging.error(f"An error occurred while inserting data: {e}")
                return False
        else:
            raise ValueError("Data parameter is empty")

    def read(self, query):
        if self.collection is None:
            logging.error("Database connection is not established. Cannot perform read operation.")
            return []

        if query is not None:
            try:
                documents = list(self.collection.find(query))
                return documents
            except errors.PyMongoError as e:
                logging.error(f"An error occurred while reading data: {e}")
                return []
        else:
            raise ValueError("Query parameter is empty")

    def update(self, query, new_values):
        if self.collection is None:
            logging.error("Database connection is not established. Cannot perform update operation.")
            return False

        if query is not None and new_values is not None:
            try:
                result = self.collection.update_many(query, {"$set": new_values})
                return result.modified_count
            except errors.PyMongoError as e:
                logging.error(f"An error occurred while updating data: {e}")
                return 0
        else:
            raise ValueError("Query or new_values parameter is empty")

    def delete(self, query):
        if self.collection is None:
            logging.error("Database connection is not established. Cannot perform delete operation.")
            return 0

        if query is not None:
            try:
                result = self.collection.delete_many(query)
                return result.deleted_count
            except errors.PyMongoError as e:
                logging.error(f"An error occurred while deleting data: {e}")
                return 0
        else:
            raise ValueError("Query parameter is empty")

