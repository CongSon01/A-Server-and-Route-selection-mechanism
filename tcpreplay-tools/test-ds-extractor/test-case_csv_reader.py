import os
import re

import numpy as np
import pandas as pd

import time
import subprocess

import argparse as arg
import concurrent.futures

CONC_THREAD = 12
SAVED_LOC = './output'
PCAP_LOC = '/home/onos/Desktop/rawds/NetFlow-QUIC1/'
OVERIDE = False

def workder_pcap_extractor(file_loc, frame_no, saved_filename_loc):
    display_filter = [f'frame.number=={frame_number}' for frame_number in frame_no]
    display_filter = ' || '.join(display_filter)
    result, err = subprocess.Popen([f'tshark -r {file_loc} -Y "{display_filter}" -w {saved_filename_loc} -q'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return saved_filename_loc, result.decode('utf-8').splitlines(), err.decode('utf-8').splitlines()

def pcap_ip_rewrite(filename):
    output_filename = f'{filename}_rewrite.pcapng'
    # subprocess.Popen(["tcprewrite", "--enet-dmac=00:00:00:00:00:01", "--enet-smac=00:00:00:00:00:02", "-i", filename, "-o", output_filename], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

def ls_subfolders(rootdir):
    sub_folders_n_files = []
    for path, _, files in os.walk(rootdir):
        for name in files:
            sub_folders_n_files.append(os.path.join(path, name))
    return sorted(sub_folders_n_files)


if __name__ == "__main__":
    lable = './label/client_merged.csv'
    lable_df = pd.read_csv(lable)
    lable_df.sort_values(['filename', 'frame_number'], inplace=True, ignore_index=True)
    pcap_loc = ls_subfolders(PCAP_LOC)

    tasks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONC_THREAD) as pool:
        for filename in lable_df['filename'].unique():

            frames_no = lable_df.loc[lable_df['filename'] == filename]['frame_number'].values
            pcap_loc_pos = [i for i, word in enumerate(pcap_loc) if word.endswith(filename.split('.')[0])]
            if len(pcap_loc_pos) == 0: continue
            file_loc = pcap_loc[pcap_loc_pos[0]]
            saved_loc_sep = os.path.normpath(file_loc).split(os.sep)[5:-1]
            saved_filename_loc = os.path.join(SAVED_LOC, *saved_loc_sep, filename.split('.')[0]) + '.pcapng'


            if os.path.exists(saved_filename_loc) and OVERIDE is False: continue
            try:
                if not os.path.exists(os.path.join(saved_filename_loc)):
                    mkdir_paths = os.path.join(SAVED_LOC, *saved_loc_sep)
                    os.makedirs(mkdir_paths)
                    print(f'''Created folder: {mkdir_paths}''')
            except FileExistsError:
                pass

            tasks.append(pool.submit(workder_pcap_extractor, file_loc, frames_no, saved_filename_loc))
            # print("waiting for tasks...", flush=True)


        for task in concurrent.futures.as_completed(tasks):
            finised_filename, result, err = task.result()
            print(finised_filename, result, err)
            # pcap_ip_rewrite(finised_filename)