#!/usr/bin/env python

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
