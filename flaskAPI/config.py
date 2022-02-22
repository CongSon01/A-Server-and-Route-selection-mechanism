import os
class DBconfig:
    mongo_uri = os.environ.get('MONGO_URL')
    database = os.environ.get('DATABASE')