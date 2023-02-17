# package capture
RABBIT_URL="10.20.0.201"

CONSUMER_QUEUE= 'raw_data'
CONSUMER_ROUTING_KEY = 'raw_data'

PRODUCER_QUEUE = 'predict_data'
PRODUCER_ROUTING_KEY = 'predict_data'

# debug result by using mongo
DEBUG = "true"
MONGO_URL = 'mongodb://10.20.0.201:27017'

# tensorflow worker
EXCHANGE = 'events'
THREADS = 4
PREFETCH_COUNT = 2 * THREADS
PADDING = 1640
BYTES_PER_PACKET = 256