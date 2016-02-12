#!/usr/bin/python
'''
Created on Oct 7, 2015

@author: michael
'''

import argparse
import argparse
import hashlib
import os.path
import shlex
import subprocess
import sys
import time

from AnalysisOutput import AnalysisOutput
from strace_parser import *
from util import *


class Strace_Analyzer:
    def __init__(self, modFile, generate_file_name=True, outfile="", scanner_location="/home/michael/scanner.jar", minecraft_dir="/home/michael/.minecraft"):
        self.STRACE_ARGS = ['-f', '-T', '-ttt', '-o']
        self.encountered_system_calls = []
        self.suspect_system_calls = []
        self.scanner_location = scanner_location
        self.modFile = modFile
        self.timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.minecraft_dir = minecraft_dir
        if generate_file_name:
            path, basefile = os.path.split(self.modFile)
#             self.modPath = path 
#             self.basefile = basefile
            outfile, hash = self.get_strace_outfile_name(basefile)
            self.outfile = outfile
#             self.outfilenamehash = hash 
        else:
            self.outfile = outfile
    
    def get_strace_outfile_name(self, modFileName):
        timestamp = self.timestamp
        fileNameTrunc = modFileName[:75]
        filenameHash = getFileNameHash(modFileName)
        storageName = fileNameTrunc+"_"+filenameHash+"_"+timestamp+".out"
        return storageName, filenameHash
    
    def get_outfile(self):
        return self.outfile
    
    def run_strace(self):
        callArgs = []
        callArgs.append("/usr/bin/strace")
        callArgs.extend(self.STRACE_ARGS)
#         path, basefile = os.path.split(modFileName)#"/home/michael/.minecraft/mods/test-1.0.jar")
#         straceOutputFile, filenameHash = self.get_strace_outfile_name(basefile)
#         callArgs.append(straceOutputFile)
        callArgs.append(self.outfile)
        callArgs.extend(["java", "-jar",self.scanner_location, "-i", self.modFile, "-l", self.minecraft_dir ])
        joinedArgs = " ".join(callArgs)
        
        shell_args = shlex.split(joinedArgs)
        print "arguments: "+str(shell_args)
        p = subprocess.Popen(shell_args)#, shell=True)
        for i in range(15):
            if p.poll() is not None:
                break
            time.sleep(1)
        if p.poll() is None:
            p.kill()
        if p.poll() != 0:
            print "error encountered when running strace"
#             sys.exit(p.poll())
        print "Finished Call----------------------------------------------"
        self.encountered_system_calls, self.suspect_system_calls = parseFile(self.outfile)
        
    def run_analyzer(self):
        self.run_strace()
        print "finished run strace"
        message = "Encountered system calls: <br />"
        for call in self.encountered_system_calls:
            message += str(call) + " "
        message += "<br /> <br />Suspect system call info:"
        for call_info in self.suspect_system_calls:
            line = "<br />"
            for info_element in call_info:
                line += str(info_element) + " "
            message += line
        print 'returning output'
        return AnalysisOutput(message, "Strace Analysis")
        
    def printEncounteredCalls(self):
        print "Encountered system calls:"
        for call in self.encountered_system_calls:
            print call 
            
    def printSuspectCalls(self):
        print "Suspect system calls:"
        for call in self.suspect_system_calls:
            print call
            
    def run(self):
        return self.run_analyzer()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--minecraft_dir", help="Location of the Minecraft directory", default="/home/michael/.minecraft")
    parser.add_argument("--scanner", help="Location of the Java jar scanner", default="/home/michael/scanner.jar")
    parser.add_argument("--file", required=True, help="File path of mod file to check")
    args = parser.parse_args()
    
    print args.file
    print os.path.isfile(args.file)
    if os.path.isfile(args.file) != True:
        print "The provided file path is not a valid file"
        sys.exit(-1)
        
    if os.access(args.file, os.R_OK) != True:
        print "File is not accessible for reading"
        sys.exit(-1)
        
    analyzer = Strace_Analyzer(args.file, scanner_location=args.scanner, minecraft_dir=args.minecraft_dir)
    
    analyzer.run()
#     print "Encountered calls:"
#     analyzer.printEncounteredCalls()
