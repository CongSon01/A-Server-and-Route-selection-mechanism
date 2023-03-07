LIFE_TIME = 70 # Thoi gian moi host chay
PERIOD = 90 # sau 90s co mot host khac ping toi server
INTERVAL = 1000 # So lan 1 host duoc thiet lap ket noi


########## iperf
# MAX_IPERF = 60000000  # flow traffict trong mang toi da ( Mb/s )
# MIN_IPERF = 20000000  # flow traffict trong mang toi thieu ( Mb/s )

########## http server MByte. Can truyen to Mbit
FILE_SIZE_MIN = 3.75 
FILE_SIZE_MAX = 15 
# MAX BANG THONG LA 10Mb

# Tren moi canh
# MAX_CAPACITY_BW = 100 # Dung luong toi da tren moi canh ( Mb/s )
MAX_CAPACITY_BW = 150 # Dung luong toi da tren moi canh ( 10Mb/s xap xi 10/8 MB)
LINK_DELAY = '100ms' # m/s thoi gian chuyen goi tin tren moi canh
LOSS_PER = 1 # % Phan tram mat mat goi tin

ARR_LOSS = [0.1, 0.2, 0.5, 1]

#sudo python3 -E run_final.py 