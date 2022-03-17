import time
import os
list_hosts = ['h4', 'h3']
for name_host in list_hosts:
    os.system('python readlog.py'+' '+name_host+' &')
    time.sleep(0.2)