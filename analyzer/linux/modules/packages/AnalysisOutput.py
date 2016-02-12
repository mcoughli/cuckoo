'''
Created on Nov 12, 2015

@author: michael
'''

class AnalysisOutput:
    def __init__(self, messageList, analysisString):
        self.messageList = messageList
        self.analysisString = analysisString
        
    def printMessage(self):
        for line in self.messageList:
            print str(line)