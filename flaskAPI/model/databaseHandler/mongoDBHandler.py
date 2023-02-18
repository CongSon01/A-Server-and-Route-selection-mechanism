from pymongo import MongoClient


class MongoDbHandler:
    """
    general class of mongo DB, any instance can be created and uses method from
    this class to access DB with specific name of database and collection
    """
    def __init__(self, database, collection):
        # uri nay co the duoc giu nguyen
        # minh chi thay doi DB va collection tuy bai toan thoi
        # con viec ket noi mongo thi connection string giu nguyen
        self.mongo_uri = "mongodb://localhost:27017"   
        self.connection = MongoClient(self.mongo_uri)
        self.database = self.connection[database]  # string name of DB
        # string name of collection
        self.collection = self.database[collection]

    def insert_many_data(self, list_data):
        """
        Insert many documents in the collection
        :param list_data: list of dictionaries (documents) to be inserted
        :return: None
        """
        if len(list_data) == 0:
            return "No data to be added"
        else:
            self.collection.insert_many(list_data)

    def insert_one_data(self, data):
        """
        Insert one document in the collection
        :param data: a dictionary (document) to be inserted
        :return: None
        """
        self.collection.insert_one(data)
        print("Insert successfully")
        return

    def update_data(self, query, update):
        """
        Update documents in the collection
        :param query: dictionary (query) to find the documents to be updated
        :param update: dictionary (update) containing the fields to be updated
        :return: None
        """
        self.collection.update_many(query, update)
        return "Update successfully"

    def remove_data(self, query):
        """
        Remove documents from the collection
        :param query: dictionary (query) to find the documents to be removed
        :return: None
        """
        self.collection.delete_many(query)
        return "Remove successfully"

    def remove_all(self):
        """
        Remove all documents in the collection
        """
        self.collection.delete_many({})
        print("All data has been removed from the collection.")

    def find_data(self, query):
        result = self.collection.find_one(query)
        if result:
            return result
        else:
            return False

    def close_connection(self):
        """
        Close the database connection
        :return: None
        """
        self.connection.close()