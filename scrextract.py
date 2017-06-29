#!/usr/bin/env python

import sys
from struct import *
import os

def deEcrpt(fname):
    f = open('A001.scr', 'r')
    of = open('of.out', 'w')

    ba = bytearray(f.read())
    bo = bytearray()

    for byte in ba:
        if byte + 128 > 255:
            bo.append(byte+128-256) #wrap
        else:
            bo.append(byte+128)

    of.write(bo)

if len(sys.argv) != 2:
    print('Usage: eveunpack <filename>')
    quit()

scr_fname = sys.argv[1]
pkd = open(scr_fname, 'rb').read()

path = sys.argv[1].split('.')[0]

if not os.path.exists(path):
    os.makedirs(path)

file_qtty = unpack('<i', pkd[4:8])[0]

def extract_all():
    for i in range(file_qtty):
        print
        pos = 8+i*40
        cur_file_rcrd = pkd[pos:pos+40]

        global file_name
        file_name = cur_file_rcrd[0:12].rstrip('\x00')
        file_start = unpack('<i', cur_file_rcrd[-4:])[0]
        file_size = unpack('<i', cur_file_rcrd[-8:-4])[0]
        file_end = file_start + file_size

        data = bytearray(pkd[file_start:file_end])
        fo = open(path + '/' + file_name, 'wb')
        fo.write(data)

def repack(file_name):
    pass
