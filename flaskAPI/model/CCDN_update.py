from pymongo import MongoClient

# mongo_uri = "mongodb://username:" + urllib.quote("p@ssword") + "@127.0.0.1:27001/"
mongo_uri = "mongodb://localhost:27017/"
connection = MongoClient(mongo_uri)

# CREATE DATABASE
database = connection['SDN_data']
# CREATE COLLECTION
collection = database['CCDN_update']
# print("Database connected")


def update_data(data_search, data_update):
    a = collection.update_many(data_search, {"$set": data_update})
    return a

def is_data_exits(data):
    return bool(collection.find(data).count() > 0)

def insert_n_data(list_data):
    if len(list_data) == 0:
        return
    else:
        collection.insert_many(list_data)

def insert_data(data):
    """
    Insert new data or document in collection
    :param data:
    :return:
    """
    collection.insert(data)
    return


def get_multiple_data():
    """
    get document data by document ID
    :return:
    """
    data = collection.find({},{'_id':0})
    return list(data)

def remove_all():
    """
    remove all documents in collection
    :return:
    """
    collection.remove({})
    return
    
# CLOSE DATABASE
connection.close()