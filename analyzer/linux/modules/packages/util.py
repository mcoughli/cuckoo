'''
Created on Oct 30, 2015

@author: michael
'''
import hashlib
import os

def getFileNameHash(fileName):
    filenameHashObj = hashlib.sha256()
    filenameHashObj.update(fileName)
    filenameHash = filenameHashObj.hexdigest()
    return filenameHash

def getFileHash(file):
    if not os.path.isfile(file):
        print "The provided file path is not a valid file"
        return ""
        
    if not os.access(file, os.R_OK):
        print "File is not accessible for reading"
        return ""
    
    hash = hashlib.sha256()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()