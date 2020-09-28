#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from werkzeug.utils import secure_filename
from flask import send_from_directory
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Excel_converter, History 
from flask import session as login_session
import random
import string
import excel
# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import pandas as pd
from tablib import Dataset
import numpy as np
import excel
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

#dataset = pd.read_csv('Data.xlsx', error_bad_lines=False)
#nx = pd.read_excel('Data.xlsx')
#pd.read_csv('Data.xlsx', error_bad_lines=False)
#lf = pd.DataFrame(nx)



#for d in lf:
    #table_names.append(d)
    
#df = pd.DataFrame(nx, columns= table_names)

#min_length = len(df[table_names])

#print len(df[table_names])
#for i in table_names:
    #for xxx in range(min_length):    
        #print(df[i][xxx])
        
        
#nx = pd.read_excel('Data.xlsx')
#lf = pd.DataFrame(nx)

engine = create_engine('sqlite:///ashtrely.db')
Base.metadata.bind = engine


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['xls', 'xlsb', 'xlsm', 'xlsx', 'xlt', 'xltx', 'xlw', 'csv'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            file_path = UPLOAD_FOLDER + "/" + filename
            nx = pd.read_excel('Data.xlsx')
            lf = pd.DataFrame(nx)

            table_names = []
#df = pd.DataFrame(nx, columns= ['Name', 'P Number', 'age', 'love','python'])

            for d in lf:
                table_names.append(d)
    
            df = pd.DataFrame(nx, columns= table_names)

            min_length = len(df[table_names])
            txt = "<style>body{height:100%;}.parent {display: flex;flex-flow: row nowrap;height: 250px;background-color:rgb(240 230 230);height:100%;align-content:center;align-items:flex-top;text-align:center;padding:10px;} .child {width: 40%;height: 40%;} .txt{ background-color: white;border:1px solid gold;padding:3px;margin:2px;} .headers {background-color: black;color:white; }</style>"
            txt += "<div class='parent'>"
            #print len(df[table_names])
            for i in table_names:
                txt += "<div class='child'>"
                txt += "<div class='txt headers'>" + str(i) + "</div>"
                for xxx in range(min_length):    
                    print(df[i][xxx])
                    txt += "<div class='txt'>"
                    txt += str(df[i][xxx])
                    txt += "</div>"
                    txt += "</br>"
                    
                txt += "</div>"
            txt += "</table>"    
                     
            
            return "upload any Excelsheet and ExcellPress will convert it for you to html flexbox template, soon you can controll the excelsheet layout and edit it "  + "<br><br>" + txt 
            ## .shape get the len of row first and second number column
            ## it our case not big deal cus our files will be all same number column and rows
            
            print("")
            array = []
            print(df.shape[0])
            for i in range(df.shape[0]):
                help0 = i
                
                for n in range(df.shape[0]):
                    help1 = n
                    print(i)
                    print(n)
                    if n > 1:
                        continue
                    print(df.iloc[help0][help1])
                    array.append(df.iloc[help0][help1])
             
            page = "<style>#request{font-family: 'Trebuchet MS', Arial, Helvetica, sans-serif;border-collapse: collapse;width:100%;}"
            page += "#request td, #request th {border: 1px solid #ddd;padding: 8px;}"
            page += "#request tr:nth-child(even){background-color: #f2f2f2;}"
            page += "#request tr:hover {background-color: #ddd;}"
            page += "#request th {padding-top: 12px;padding-bottom: 12px;text-align: left;background-color: #4CAF50;color: white;}"
            page +="</style>"
            page += "<table id='request'><tr><th>Name</th><th>P Number</th></tr>"
            
            print(len(array))
            ## here we change 2 by the cells number we already must know how many cells
            ## in the request or how many fileds don't forget always divide by the cells number 

            cells_index = 0
            got_it = False
            ages = []
            for onetd in range(len(array)):
                help2 = onetd
                
                if onetd % 2 == 1:
                    ages.append(array[onetd])
                    page += "<td>" + str(array[onetd]) + "</td>"

                else:
                    page += "</tr><tr>" + "<td>" + str(array[onetd]) +  "</td>"                 

            return page

            
                                    
    return render_template('index.html')








@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080, threaded=False)
