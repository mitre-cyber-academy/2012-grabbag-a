#!/usr/bin/env python

# Author: Stephen DiCato
# Created for the MITRE CTF

import sys
import time
import zipfile
from random import randint

def create():
    '''
    Create a zip file with a hidden message buried in the zipinfo comments
    '''
    zf = zipfile.ZipFile('challenge.zip', mode = 'w')

    comments = []
    try:
        with open('flag.txt', 'r') as f:
            comments = list(f.read())

    except IOError as e:
        print "Can't open the flag.txt file to create the zip"
        sys.exit(1)

    filenames = []
    current = 'README.txt'
    filenames.append(current)
    
    for i in xrange(len(comments)):
        if i == len(comments) - 1:
            info = zipfile.ZipInfo(current, 
                                   date_time=time.localtime(time.time()),
                                   )
            info.comment = comments[i]
            info.create_system=0
            zf.writestr(info, "Check the comments!")
            break
            
        while 1:
            nextfile = str(randint(0, len(comments))) + '.txt'
            if nextfile not in filenames:
                break

        filenames.append(nextfile)
        info = zipfile.ZipInfo(current, 
                               date_time=time.localtime(time.time()),
                               )
        info.comment = comments[i]
        info.create_system=0
        zf.writestr(info, "The next is %s" % str(nextfile))
        current = nextfile

    zf.close()

def solve():
    '''
    Pull a hidden message out of zipinfo comments
    '''
    zf = zipfile.ZipFile('challenge.zip')
    f = zf.open('README.txt')
    current = [x.strip() for x in f.read().split(' ')][-1]

    comments = []
    while 1:
        try:
            f = zf.open(current)
        except KeyError:
            break

        next  = [x.strip() for x in f.read().split(" ")][-1]
        comments.append(zf.getinfo(current).comment)
        current = next

    print ''.join(comments)

if __name__ == "__main__":

    if sys.argv[1] == 'create':
        create()
    elif sys.argv[1] == 'solve':
        solve()
        
