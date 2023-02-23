#!/home/onos/Documents/Github/venv10/bin/python3

'''
    This script is used to play pcap files on a mininet network
    Meant to be used in mininet hosts
'''

import os, sys
import subprocess
import time                                                                                                                    
import logging

import requests as rq
import json

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread
import uvicorn

app = FastAPI()
logging.basicConfig(filename='pcap-player.log', level=logging.INFO)

def ls_subfolders(rootdir):
    sub_folders_n_files = []
    for path, _, files in os.walk(rootdir):
        for name in files:
            sub_folders_n_files.append(os.path.join(path, name))
    return sorted(sub_folders_n_files)

def ls_file_in_current_folder(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def ls_folder_in_current_folder(path):
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

# split folder
fd = ls_subfolders('/home/onos/Desktop/output_rewrite/')
# folders = [os.path.split(f)[0] for f in fd]
# files = [os.path.split(f)[1] for f in fd]

class ServicePcap(BaseModel):
    service_name: str
    # pcap_file: str
    src_name: str
    # src_ip: str
    dst_name: str
    # dst_ip: str

@app.post("/play_pcap")
async def play_pcap(service_pcap: ServicePcap):
    store_path = '/home/onos/Desktop/output_rewrite/'    
    service_path = f'{store_path}{service_pcap.service_name}/'
    
    process_time = {}
    for folder in ls_folder_in_current_folder(service_path):
        for file_path in ls_subfolders(
            os.path.join(service_path, folder,
                         f'{service_pcap.src_name}-{service_pcap.dst_name}')):
            start_time = time.time()
            data = {
                'file': file_path,
                'start_time': start_time,
            }
            # rq.post(f'http://{service_pcap.dst_ip}:8000/ping', 
            #         headers={'Content-Type': 'application/json'}, data=json.dumps(data))
            file_path = os.path.join(service_path, folder, file_path)
            print(f"start replay !!! {file_path}")
            result = subprocess.Popen(f'echo "rocks@123" | sudo -S -k tcpreplay -i s5-eth10 -K {file_path}', 
                                      shell=True, stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE).communicate()
            end_time = time.time()
            print(f'start time: {start_time}, end time: {end_time}, process time: {end_time - start_time}')
            process_time[file_path] = {
                'start_time': start_time,
                'end_time': end_time,
                'process_time': end_time - start_time
            }
            # logging.INFO(f'Played file {file_path}, start time: {start_time}, end time: {end_time}, process time: {end_time - start_time}')
            # delay between each file
            time.sleep(5)
    return {
        'result': result[0],
        'error': result[1],
        'process_time': process_time
    }

# global server_config
# class ServerConfig(BaseModel):
#     server_config: dict

# @app.post('/server_config')
# async def server_config(server_config: ServerConfig):
#     server_config = server_config.server_config 
#     return {
#         'server_config': 'server_config'
#     }

class ServerLatency(BaseModel):
    file: str
    server_start_time: float
    respone_time_1: float

server_respone_time = {}

@app.post("/respone_time")
async def respone_time(server_latency: ServerLatency):
    respone_time = respone_time.server_start_time - time.time() + respone_time.respone_time_1
    server_respone_time[server_latency.file] = {
        'respone_time': respone_time
    }
    return {
        'sv_r': server_latency.server_send_time,
        'latency': server_latency.server_send_time - time.time()
    }

@app.get('/')
async def hello():
    return {
        'hello': 'world'
    }

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)