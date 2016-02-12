'''
Created on Oct 20, 2015

@author: michael
'''
import sys

concerning_syscalls = ["execve", "open", "access", "stat", "fstat", "mmap", "lstat"]

def parseLine(line):
    syscall_time, seperator, remaining = line.partition(" ")
    timestamp, seperator, syscall_total = remaining.partition(" ")
#     print "Syscall time: "+str(syscall_time)
#     print "Timestamp: "+str(timestamp)
#     print "Syscall: "+str(syscall_total)
    resumed = False
    exited = False
    if syscall_total.startswith("<... "):
        syscall_total = syscall_total.replace("<... ", "", 1)
        syscall, seperator, remaining = syscall_total.partition(" ")
        resumed = True
    elif syscall_total.find("+++ ") == 0:
        syscall_total = syscall_total.replace("+++ ", "", 1)
        syscall, seperator, remaining = syscall_total.partition(" ")
    elif syscall_total.find("--- ") == 0:
        syscall_total = syscall_total.replace("--- ", "", 1)
        syscall, seperator, remaining = syscall_total.partition(" ")
    else:
        syscall, seperator, remaining = syscall_total.partition("(")
    return syscall, syscall_time, timestamp, syscall_total, resumed, exited
    

#TODO: better handling of files
def parseFile(filename):
    strace_file = open(filename)
    system_calls = []
    encountered_system_calls = set()
#     for line in strace_file:
    i = 0
    for line in strace_file:
        syscall_info = parseLine(line)
        if syscall_info[0] in concerning_syscalls:
            system_calls.append(syscall_info)
        encountered_system_calls.add(syscall_info[0])
#         i = i+1
#         if i == 10:
#             break
    return sorted(encountered_system_calls), system_calls
    
    
if __name__ == '__main__':
    parseFile(sys.argv[1])