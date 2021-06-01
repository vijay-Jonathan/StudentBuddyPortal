from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mail import Mail,Message
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
import os
from urllib.request import urlopen 
import urllib
import shutil
from bs4 import BeautifulSoup
import requests
from flask import *
import joblib



import pickle
import numpy as np

app=Flask(__name__)


app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='chatbot'
app.config['MYSQL_CURSORCLASS']='DictCursor'

app.config.from_pyfile('config.cfg')
mail=Mail(app)

s=URLSafeTimedSerializer('secret123')

mysql=MySQL(app)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/feedback')
def feedback():
	return render_template('feedback.html')
    
@app.route('/placement')
def placement():
	return render_template('placement.html')

    
@app.route('/chatbot')
def bot():
	return render_template('bot.html')






def placepred(x):
    k =[x]
    loaded_model = joblib.load('placement_model.pkl')
    precio=loaded_model.predict(k)
    print(precio)
    if precio < 350000:
        rta = "Predicted Placement range is 0 to 3.5LPA" 
    elif precio >= 350000 and precio < 800000:
        rta = "Predicted Placement range is 3.5 to 8LPA" 
    else:
        rta = "Predicted Placement range is greater than 8LPA"        
    print(rta)
    return rta

@app.route('/long',methods=['GET','POST'])
def long():
    dat=[]

    if request.method == 'POST':
        cgpa = request.form['cgpa']
        tot_arriers= request.form['tot_arriers']
        clrd_arriers = request.form['clrd_arriers']
        intern = request.form['interns']
        paidintern = request.form['Paid_intrn']
        project = request.form['Projects']
        articles = request.form['Articels']	
        dat  =[cgpa,tot_arriers,clrd_arriers,intern,paidintern,project,articles]
        intmap=map(int,dat)
        l=list(intmap)
        print(l)
        # print(dat)
        pp = placepred(l)
        print("-----------------",pp)
    return render_template('placement.html',pp=pp)


@app.route('/bot',methods=['GET','POST'])
def botpre():
    dat=[]

    if request.method == 'POST':
        # cgpa = request.form['cgpa']
        # tot_arriers= request.form['tot_arriers']
        # clrd_arriers = request.form['clrd_arriers']
        # intern = request.form['interns']
        # paidintern = request.form['Paid_intrn']
        # project = request.form['Projects']
        # articles = request.form['Articels']	
        # dat  =[cgpa,tot_arriers,clrd_arriers,intern,paidintern,project,articles]
        # intmap=map(int,dat)
        # l=list(intmap)
        # print(l)
        # # print(dat)
        # pp = placepred(l)
        op ="Click on this ink to open AUMS https://intranet.cb.amrita.edu/aums"
        print("-----------------",op)
    return render_template('bot.html',op=op)


@app.route('/submit',methods=['GET','POST'])
def submit_feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        rollno = request.form['rollno']
        platfrom = request.form['platfrom']
        message = request.form['message']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO feedback(name,email,rollno,platform,message) VALUES(%s,%s,%s,%s,%s)",(name,email,rollno,platfrom,message))
        mysql.connection.commit()
        cur.close()
        flash("Thank you for submiting your feedback")
        
    return render_template('feedback.html')



if __name__=='__main__':
	app.secret_key='secret123'
	app.run(debug=True, host='127.0.1.1')

