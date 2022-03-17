import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["SDN_data"]
mycol = mydb["BW_server"]


def insert_one(data):
    """
    Insert new data or document in collection
    :param data:
    :return:
    """
    mycol.insert(data)
    return

def insert_data(list_BW):
    if len(list_BW) == 0:
        return
    else:
        mycol.insert_many(list_BW)