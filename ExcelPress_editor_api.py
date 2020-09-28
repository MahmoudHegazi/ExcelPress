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
            nx = pd.read_excel(file_path)
            lf = pd.DataFrame(nx)

            table_names = []
#df = pd.DataFrame(nx, columns= ['Name', 'P Number', 'age', 'love','python'])

            for d in lf:
                table_names.append(d)
    
            df = pd.DataFrame(nx, columns= table_names)

            min_length = len(df[table_names])
            txt = "<style>body{height:100%;}.parent {display: flex;flex-flow: row nowrap;height: 250px;background-color:rgb(240 230 230);height:100%;align-content:center;align-items:flex-top;text-align:center;padding:10px;} .child {width: 40%;height: 40%;} .txt{ background-color: white;border:1px solid gold;padding:3px;margin:2px;} .headers {background-color: black;color:white; }</style>"
            #txt += "<script>const tb_color = document.getElementById('table_background');cb_color = document.getElementById('cell_background');"
            #txt += "let current_tbcolor = document.querySelector('.parent');"
            #txt += " function play() {alert(current_tbcolor.style.background);} " 
            #txt += "<script>function play(){window.addEventListener('DOMContentLoaded', (event) => { alert(x); })"
            #txt += "</script>"


            
            txt += "<label for='tback'>Table Background-color: </label>"
            txt += "<input name='tback' id='table_background' type='color' onclick='play()'> <br><br>"
            txt += "<label for='cback'>Cells Background-color: </label>"
            txt += "<input name='cback' id='cell_background' type='color'>"
            txt += "<div class='parent'>"
            #print len(df[table_names])
            for i in table_names:
                txt += "<div class='child'>"
                txt += "<div class='txt headers'>" + str(i) + "</div>"
                for xxx in range(min_length):    
                    print(df[i][xxx])
                    txt += "<div class='txt' style='color:lightblue;' >"
                    txt += str(df[i][xxx])
                    txt += "</div>"
                    txt += "</br>"
                                
                                
                                
                txt += "</div>"
            txt += "</table>"
            txt += "<script>"
            txt += "window.addEventListener('DOMContentLoaded', (event) => {window.addEventListener('click', (event) => {let table_background = document.querySelector('.parent');let tbk_input = document.getElementById('table_background');table_background.style.background = tbk_input.value; let cell_background = document.querySelectorAll('.txt');let cbk_input = document.getElementById('cell_background');cell_background.forEach( (element) =>{element.style.background = cbk_input.value;})}) })</script>"
            
            print table_names
            
            return "upload any Excelsheet and ExcellPress will convert it for you to html flexbox template, soon you can controll the excelsheet layout and edit it "  + "<br><br>" + txt 
            ## .shape get the len of row first and second number column
            ## it our case not big deal cus our files will be all same number column and rows

    return render_template('index.html')








@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080, threaded=False)
