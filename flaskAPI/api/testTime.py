import time
starttime = time.time()

# print str after 2 minutes
while True:
    # print(starttime)
    # print(time.time() - starttime)

    if time.time() - starttime > 3:
        print("Time out")
        starttime = time.time()

