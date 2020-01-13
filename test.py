#!/home/oleg/.local/bin/python3_virt/bin/python3

from os import listdir
from os.path import isfile, join
from os import curdir, sep
import os
import pathlib

target_folder = os.getenv('CREDENTIALS_FOLDER', 'creds')


def get_credentials(target_folder):
    try:
        path = pathlib.Path(__file__).parent / target_folder
        files = [f for f in listdir(path) if isfile(join(path, f))]
        credentials = {}
        for file in files:
            with open(curdir + sep + target_folder + sep + file, 'r') as procfile:
                content = procfile.read().replace('\n', '')
                procfile.close()
                credentials[file] = content
    except IOError:
        print("Invalid target folder!")
        exit(101)
    return credentials


print (get_credentials(target_folder))
