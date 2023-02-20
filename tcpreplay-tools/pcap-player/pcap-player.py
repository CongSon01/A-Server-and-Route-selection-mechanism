import os, sys
import subprocess

'''
    This script is used to play pcap files on a mininet network
    Meant to be used in mininet hosts
'''
virtualenv = '../../venv10/bin/python3'

def main():
    cmd = f'{virtualenv} '
    pass

if __name__ == main():
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
