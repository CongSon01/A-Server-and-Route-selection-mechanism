import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["SDN_data"]
mycol = mydb["ServerCost"]

def insert_n_data(list_BW):
    if len(list_BW) == 0:
        return
    else:
        mycol.insert_many(list_BW)

def insert_data(data):
    """
    Insert new data or document in collection
    :param data:
    :return:
    """
    mycol.insert(data)
    return
    
def get_multiple_data():
    """
    get document data by document ID
    :return:
    """
    data = mycol.find()
    return list(data)

def remove_all():
    """
    remove all documents in collection
    :return:
    """
    mycol.remove({})
    return
    
# CLOSE DATABASE
myclient.close()