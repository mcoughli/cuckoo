'''
Created on Feb 6, 2016

@author: michael
'''
import os
import threading
from lib.common.abstracts import Package
from lib.api.process import Process as cuckooProcess
from strace_analyzer import Strace_Analyzer
from multiprocessing import Process as mProcess
import time
from util import *
import logging

log = logging.getLogger(__name__)

class Classloader(Package):
    '''
    classdocs
    '''


    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        Package.__init__(self, *args, **kwargs)
#         self.seen_pids = set()
        self.scanner_finished = False
        self.lock = threading.Lock()
        
    def check(self):
        self.lock.acquire()
        scanner_current = self.scanner_finished
        self.lock.release()
        if scanner_current == True:
            return False
        else:
            return True
    
    def get_strace_outfile_name(self, modFileName):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        path, basefile = os.path.split(modFileName)
        fileNameTrunc = basefile[:75]
        filenameHash = getFileNameHash(basefile)
        storageName = fileNameTrunc+"_"+filenameHash+"_"+timestamp+".out"
        return storageName, filenameHash
        
    def start(self, path):
        print 'test'
        self.analyzer_outfile = self.get_strace_outfile_name(path)[0]
        print 'test2'
#         scanner = self.options['scanner']
        scanner = "/home/cuckoo/scanner.jar"
        if scanner is None:
            scanner = "/home/cuckoo/scanner.jar"
        minecraft_dir = self.options['minecraft']
        if minecraft_dir is None:
            minecraft_dir = '~/.minecraft'
        
        analyzer = Strace_Analyzer(path, generate_file_name=False, outfile=self.analyzer_outfile, scanner_location=scanner, minecraft_dir=minecraft_dir)
#         mExecutor = mProcess(target=analyzer)
#         mExecutor.start()
#         cWatcher = cuckooProcess(pid=mExecutor.pid())
        analyzer.run()
        self.lock.acquire()
        self.scanner_finished = True
        self.lock.release()
        
    def package_files(self):
        wd = os.getcwd()
#         file = str(wd) + "/" + str(self.analyzer_outfile)
        log.debug("TEST!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        log.debug(self.analyzer_outfile)
        return [(self.analyzer_outfile, self.analyzer_outfile)]
        
        
        
        
        