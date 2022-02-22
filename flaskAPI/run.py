#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time

import threading
import concurrent.futures
import subprocess as sp

PROGRAM_LIST = [
    {
        "name": "example2.py",
        "path": "./run/",
        "launch": "python3",
        "flag": ""
    },
    {
        "name": "app.py",
        "path": "./api/",
        "launch": "python3",
        "flag": ""
    },
    {
        "name": "uppdateWeight.py",
        "path": "./api/",
        "launch": "python3",
        "flag": ""
    }
]


CWD_PATH = os.getcwd()

def build_param(program: dict):
    program['name']
    program['launch']
    program['path']
    program['flag']
    param = program['launch'] + " " + program['path'] + \
            program['name'] + " " + program["flag"]
    return [param]
    

# append function to list
# https://queirozf.com/entries/python-3-subprocess-examples#call-example-capture-stdout-and-stderr
if __name__ == '__main__':
    
    threads = []
    
    for program in PROGRAM_LIST:
        sp.run(build_param(program), check=True, shell=True, stdout=sp.PIPE)
            
