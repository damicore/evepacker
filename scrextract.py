#!/usr/bin/env python

import sys
from struct import *
import os

#clean and learn about python bitwise operations
def decrypt(data):
    bo = bytearray()
    for byte in data:
        if byte + 128 > 255:
            bo.append(byte+128-256) #wrap
        else:
            bo.append(byte+128)
    return bo

def extract_all():
    global pkd
    file_qtty = unpack('<i', pkd[4:8])[0]

    for i in range(file_qtty):

        pos = 8+i*40
        cur_file_rcrd = pkd[pos:pos+40]

        file_name = cur_file_rcrd[0:12].rstrip('\x00')
        file_start = unpack('<i', cur_file_rcrd[-4:])[0]
        file_size = unpack('<i', cur_file_rcrd[-8:-4])[0]
        file_end = file_start + file_size

        data = bytearray(pkd[file_start:file_end])
        if file_name[-4:] == '.SCR':
            print('Unencrypting')
            data = decrypt(data)
        fo = open(path + '/' + file_name, 'wb')
        fo.write(data)

def repack(fn):
    file_to_insert = open(fn, 'rb').read()
    global pkd
    file_qtty = unpack('<i', pkd[4:8])[0]
    delta = 0
    found = False
    for i in range(file_qtty):
        pos = 8+i*40
        cur_file_rcrd = pkd[pos:pos+40]
        file_name = cur_file_rcrd[0:12].rstrip('\x00')
        file_start = unpack('<i', cur_file_rcrd[-4:])[0]
        if found == True:
            cur_file_rcrd[-4:] = file_start + delta #THIS IS WRONG!!!! DOESNT MODIFY PKD
            #edit current file record
            pass
        if file_name == fn:
            found = True
            old_filesize = unpack('<i', cur_file_rcrd[-8:-4])[0]
            new_file_size = len(file_to_insert)
            old_file_end = file_start + old_file_size
            delta = new_file_size - old_file_size
            data = bytearray(file_to_insert)
            if file_name[-4:] == '.SCR':
                data = decrypt(data)
            ending_chunk = pkd[old_file_end:] #original ending of file
            beginning_chunk = pkd[0:file_start]
            pkd = beginning_chunk.append(data).append(ending_chunk)
            cur_file_rcrd[-8:-4] = new_file_size #updating filesize
            pass


        fo = open(path + '/' + 'scr.pkd', 'wb') #generalizar con filename
        fo.write(pkd)

if len(sys.argv) != 2:
    print('Usage: eveunpack [option] <filename>')
    print('where option is -e (for extract) -i (for insert)')
    quit()

#scr_fname = sys.argv[1]
pkd = open('scr.pkd', 'rb').read() #scr_fname

path = sys.argv[1].split('.')[0]

if not os.path.exists(path):
    os.makedirs(path)

# todo: handle switches
# extract_all()
repack(sys.argv[1])
