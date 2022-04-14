import time
ok_time = 0
def A():
    global ok_time
    time_start = time.time()
    for i in range(100):
        # print(i)
        a = 1 + 1
    ok_time = time.time() - time_start 
    print(ok_time)

def B():
    global ok_time
    print(ok_time)
A()
A()
A()
A()
A()
A()
B()