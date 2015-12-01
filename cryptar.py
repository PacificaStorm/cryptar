#usr/bin/env python
# -*- coding : utf-8 -*-

import math
import numpy
from Crypto.Cipher import AES
import base64
import os
import binascii
from base64 import b64encode

mode = raw_input("Would you like to DI or open an audio file? Type DI or FILE:  ")
if mode=="DI":
    print("Sorry, this mode is not currently functioning. Try again later")
    quit()
elif mode!="FILE":
    print("That is not a valid mode. Try again later")
    quit()
else:
    fil = raw_input("Please name the file you want to open:  ")
command = ["aubiopitch", "-i", fil, "> test.txt"]
command2 = "aubiopitch -i " + fil + " > test.txt"
import subprocess
subprocess.call(command2, shell=True)

try:
    ### opening aubiopitch output file
    with open("test.txt") as f:
        content = f.readlines()
    freqArray = []
    for i in content:
        ### extracting the frequency from the data
        a = i.split()
        b = a[1]
        c = b.split(".")
        d = c[0]
        freq = int(d)
        if freq>15:
            freqArray.append(freq)
    

    ### splitting array into seconds
    freqComposite = [freqArray[x:x+43] for x in range(0, len(freqArray), 43)]
    
    ### limiting number of notes to 4
    
    freqComposite = freqComposite[:4]
    
    ### removing the outliers

    def removeOutliers(n):
        if abs(n - dur) <= stdTest:
            return(n)
    
    freqFiltered = []

    for k in freqComposite:
        dur = numpy.mean(k)
        stdTest = numpy.std(k)

        k = filter(removeOutliers, k)
        
        freqFiltered.append(k)
    
    ### getting average frequency for each second
    freqAvg = []
    for l in freqFiltered:
        avg = sum(l)/len(l)
        freqAvg.append(avg)
    

    ### generating the key
    if len(freqAvg)==0:
        raise ValueError("Frequencies were not generated. Check the audio file")
    elif len(freqAvg)==1:
        encKey = str(freqAvg[0])
    elif len(freqAvg)==2:
        encKey = str(freqAvg[0])+str(freqAvg[1])
    elif len(freqAvg)==3:
        encKey = str(freqAvg[0])+str(freqAvg[1])+str(freqAvg[2])
    else:
        encKey = str(freqAvg[0])+str(freqAvg[1])+str(freqAvg[2])+str(freqAvg[3])
    if len(encKey)%2!=0:
        encKey = encKey + "a"
    while len(encKey)<32:
        encKey = encKey*2
    
    encKey = encKey[:32]
       
        

    def encryption(secretinfo):
        BLOCK_SIZE=16
        PADDING= '{'

        pad= lambda s: s +( BLOCK_SIZE - len(s) % BLOCK_SIZE)* PADDING

        EncodeAES= lambda c, s :base64.b64encode(c.encrypt(pad(s)))

        convert= binascii.unhexlify(encKey)
        secret= convert
        cipher=AES.new(secret)

        encoded=EncodeAES (cipher, secretinfo)
        #print 'Encrypted string:' , encoded
        try:
            outEnc = open("message.txt", "w")
            outEnc.write(encoded)
        finally:
            outEnc.close()

    def decryption (encryptedString):
        PADDING= '{'
        DecodeAES= lambda c, e:c.decrypt(base64.b64decode(e)).rstrip(PADDING)
        key= binascii.unhexlify(encKey)
        cipher= AES.new(key)
        decoded = DecodeAES(cipher, encryptedString)
        print decoded


    ask= raw_input( ' Would you like to (E)ncrypt or (D)ecrypt?: ')
    if ask =='E':
        variable= raw_input(' What is your message? ')
        encryption(variable)
    elif ask=='D':
        #message= raw_input ( ' Please Enter your Encrypted Message: ')
        try:
            inEnc = open("message.txt", "r")
            message = inEnc.read()
        finally:
            inEnc.close()
        decryption(message)

finally:
    f.close()
