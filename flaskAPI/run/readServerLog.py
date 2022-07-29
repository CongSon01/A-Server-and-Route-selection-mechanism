import sys
# sys.path.append('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/model')
sys.path.append('/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/model')
import Server_Info, Server_Info_Full
import ast
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

def find_sub_string(start, end, text):
    start_index, end_index = 0, 0
    try:
        start_index = text.index(start)
        end_index = text.index(end)
    except:
        print("Tim chuoi that bai")

    return text[start_index: end_index + 1]

def get_server_info(file_name, name_host):
    logfile = open(file_name)
    loglines = follow(logfile)
    results = []
    for line in loglines:
        if line[0] == '{':
            data = ast.literal_eval(find_sub_string('{', '}', line))
            print("SERVER INFO: ", data)
            # try:
            Server_Info_Full.insert_data(data)
            if ('_id' in data.keys()):
                del data['_id']
            if Server_Info.is_data_exit(data['server_ip']):
                Server_Info.update_many(data['server_ip'], data)
            else:
                Server_Info.insert_data(data)
            
            
    logfile.close()
    
print("Get server info")
path = '/home/onos/Downloads/A-Server-and-Route-selection-mechanism/flaskAPI/run/server_info/' + sys.argv[1] + '.txt'
list_BW = get_server_info(path, sys.argv[1])