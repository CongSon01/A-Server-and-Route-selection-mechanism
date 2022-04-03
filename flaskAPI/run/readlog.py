import sys
sys.path.append('/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/model')
import BW_server

import time
import sys

# def update_server():
#     output(sys.argv[1])

# from __future__ import print_function
def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line

# def output(file):
#     logfile = open(file)
#     loglines = follow(logfile)
#     for line in loglines:
#         print(line, end='')
#         list_col = line.split()
#         if list_col[0] == '[SUM]':
#             # new_df = { 'Transfer': list_col[4], 'Bandwidth': list_col[6], 'Jitter': list_col[8], 'Lost': list_col[10], 'Total': list_col[9], 'Datagrams': list_col[10] }
#             # print(list_col)
#             # if list_col[0][-1] == '-':
#             if len(list_col) == 13:
#                 new_df =  [float(list_col[4]), float(list_col[6]), float(list_col[8]), float(list_col[10][:-1]), float(list_col[11]), float(list_col[12][1:-2]) ]
#             elif len(list_col) == 12:
#                 new_df = [float(list_col[3]), float(list_col[5]), float(list_col[7]),  float(list_col[9][:-1]), float(list_col[10]), float(list_col[11][1:-2])]
#             else:
#                 continue
#             # df_final.append(new_df)
#             print(new_df)
            
#     logfile.close()
# # output(sys.argv[1])
# output("test.txt")

def get_BW_from_server(file_name, name_host):
    logfile = open(file_name)
    loglines = follow(logfile)
    results = []
    for line in loglines:
        list_col = line.split()
        # print(list_col)
        if list_col[0] == '[SUM]':
                # new_df = { 'Transfer': list_col[4], 'Bandwidth': list_col[6], 'Jitter': list_col[8], 'Lost': list_col[10],'Total': list_col[9], 'Datagrams': list_col[10] }
                # print(list_col)
                # if list_col[0][-1] == '-':
            if len(list_col) == 13:
                results = [{"Servername":name_host,"Bandwidth":float(list_col[6])}]
                    # new_df =  [float(list_col[4]), float(list_col[6]), float(list_col[8]), float(list_col[10][:-1]), float(list_co[11]), float(list_col[12][1:-2]) ]
            elif len(list_col) == 12:
                results = [{"Servername":name_host,"Bandwidth":float(list_col[5])}]
                    # new_df = [float(list_col[3]), float(list_col[5]), float(list_col[7]),  float(list_col[9][:-1]), float(list_co[10]), float(list_col[11][1:-2])]
            else:
                continue
            # CALL API
            # print(results)
            BW_server.insert_data(results)
            
    logfile.close()
    
path = '/home/onos/Downloads/flask_SDN/Flask-SDN/flaskAPI/run/' + sys.argv[1] + '.txt'
list_BW = get_BW_from_server(path, sys.argv[1])
# BW_server.insert_data(list_BW)