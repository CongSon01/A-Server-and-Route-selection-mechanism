import sys
sys.path.append('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/model')
import ServerCost

import time
import sys

# Doc Bang thong tu background ipef

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line

def get_BW_from_server(file_name, name_host):
    logfile = open(file_name)
    loglines = follow(logfile)
    results = []
    for line in loglines:
        list_col = line.split()
        # print(list_col[6])
        if list_col[0] == '[SUM]':
            try:
                if len(list_col) == 13 :
                    results = [{"Servername":name_host,"Bandwidth":float(list_col[6])}]
                        # new_df =  [float(list_col[4]), float(list_col[6]), float(list_col[8]), float(list_col[10][:-1]), float(list_co[11]), float(list_col[12][1:-2]) ]
                elif len(list_col) == 12 :
                    results = [{"Servername":name_host,"Bandwidth":float(list_col[5])}]
                        # new_df = [float(list_col[3]), float(list_col[5]), float(list_col[7]),  float(list_col[9][:-1]), float(list_co[10]), float(list_col[11][1:-2])]
                else:
                    continue
                # CALL API
                # print(results)
                # print("chen vao mongooooooooooooooooooooooo")
                ServerCost.insert_data(results)
                # print("Ghi server Cost thanh cong")
            except:
                print("error write BW to mongodb")
            
            
    logfile.close()
    
print("GHI FILE BW")
path = '/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/run/BW_server/' + sys.argv[1] + '.txt'
list_BW = get_BW_from_server(path, sys.argv[1])