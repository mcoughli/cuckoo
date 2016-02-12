'''
Created on Oct 30, 2015

@author: michael
'''

from flask import Flask, url_for, request, redirect, g
from werkzeug.utils import secure_filename
import pickle
import os
from strace_analyzer import Strace_Analyzer
import tempfile
import sqlite3

#Config:
REPORT_TABLE_OBJ_FILENAME = 'reports_table.pkl'
ALLOWED_EXTENSIONS = set(['jar'])
DATABASE = '../Minecraft_Service_Private/mod_reports.db'

app = Flask(__name__)
reports_table = dict()
def setup_app():
    if os.path.exists(REPORT_TABLE_OBJ_FILENAME):
        reports_table = pickle.load(REPORT_TABLE_OBJ_FILENAME)

setup_app()
app.config['REPORT_TABLE_OBJ_FILENAME'] = REPORT_TABLE_OBJ_FILENAME
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

def connect_to_database():
    #TODO: make the database connection more secure maybe? All the data 
    #in the database will be public anyway, but maybe?
    db = sqlite3.connect(DATABASE)
    db.execute('CREATE table if not exists AnalyisFiles ()')
    return 

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print 'received file'
        file = request.files['file']
        if file and allowed_file(file.filename):
            print 'allowed file'
            filename = secure_filename(file.filename)
            tempfolder = tempfile.mkdtemp()
            file.save(os.path.join(tempfolder, filename))
            filepath = tempfolder + "/" + filename
            process_file(filename, filepath)
            return redirect(url_for('printReport',
                                    analysisKey=filename))
        else:
            return "Illegal file type"
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

def updateTableEntry(analysisKey, report):
    print 'updating entry'
    if analysisKey in reports_table:
        print 'not in table'
        reports_table[analysisKey].append(report)
        print 'added to table'
    else:
        reports_table[analysisKey] = list([report])
#     pickle.dump(reports_table, app.config['REPORT_TABLE_OBJ_FILENAME'])
 
def process_file(filename, filepath):
    processor_modules = ['Strace_Analyzer()']
    print 'processing'
    for analyzer_str in processor_modules:
        analyzer = eval(analyzer_str)
        print 'evalled'
        output = analyzer.run_analyzer(filepath)
        print 'eval finished'
        updateTableEntry(filename, output)
 
@app.route('/')
def hello_world():
    message = 'Hello! Please upload a minecraft jar here:'
    message += "<br /><a href=\"" + str(url_for('upload_file')) +"\">Upload file</a>"
    return message

@app.route('/reports/<analysisKey>')
def printReport(analysisKey):
    if analysisKey in reports_table:
        reportList = reports_table[analysisKey]
        sorted_reports = sorted(reportList, key=lambda x: x.analysisString)
        message = ""
        for report in sorted_reports:
            message += str(report.analysisString)
            message += "\n"
            message += str(report.messageList)
        return message
    else:
        return "Report does not exist"
    

@app.route('/reports')
def reports():
    message = 'Reports:'
    for report_key in reports_table:
        message += "<br />" + str(url_for(printReport, report=report_key))
    return message
        
    

if __name__ == '__main__':
    app.run(debug=True)