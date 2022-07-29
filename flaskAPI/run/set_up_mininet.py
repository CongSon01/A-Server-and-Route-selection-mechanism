LIFE_TIME = 70 # Thoi gian moi host chay
PERIOD = 90 # Random Thoi gian chay cua host
INTERVAL = 1000 # So lan 1 host duoc xuat phat
MAX_IPERF = 60000000  # flow traffict trong mang toi da ( Mb/s )
MIN_IPERF = 20000000  # flow traffict trong mang toi thieu ( Mb/s )
FILE_SIZE_MIN = 10 # MG Byte 
FILE_SIZE_MAX = 60 # MG Byte 
# MAX BANG THONG LA 25MG Byte

# Tren moi canh
# MAX_CAPACITY_BW = 100 # Dung luong toi da tren moi canh ( Mb/s )
MAX_CAPACITY_BW = 800 # Dung luong toi da tren moi canh ( 800Mb/s xap xi 100 MB)
LINK_DELAY = '3ms' # m/s thoi gian chuyen goi tin tren moi canh
LOSS_PER = 1 # % Phan tram mat mat goi tin

ARR_LOSS = [0.1, 1, 2, 5]

#sudo python3 -E run_final.py 