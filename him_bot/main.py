"""
    Himanshu Gwalani
    2017ucp1356
"""
from core import Cli,utils,Settings,db
from core.color import *
from sys import version_info as py_ver
import argparse,os

def main():
    
    # get path of stored file /test/Desktop/....
    Settings.path = os.getcwd()

    
    Cli.start()
    sys.exit()

if __name__ == '__main__':
    main()
