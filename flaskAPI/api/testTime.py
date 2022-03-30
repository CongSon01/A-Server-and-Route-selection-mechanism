import time
starttime = time.time()
# print str after 2 minutes
print('start time: ' + str(starttime))

if time.time() - starttime > 120:
    print("Time out")
print('end time: ' + str(time.time()))

