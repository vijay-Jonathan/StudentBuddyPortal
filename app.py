from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mail import Mail,Message
from flask_mysqldb import MySQL
# from wtforms import Form,StringField,TextAreaField,PasswordField,validators
# from passlib.hash import sha256_crypt
from functools import wraps
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
# import os
# from urllib.request import urlopen 
# import urllib
# import shutil
# from bs4 import BeautifulSoup
# import requests
from flask import *
import joblib

# ======================
# !pip install tensorflow
# !pip install tensorflow_hub
# !pip install gensim
# import logging
# logging.getLogger("tensorflow").setLevel(logging.WARNING)
import tensorflow_hub as hub
import tensorflow as tf

# from gensim.test.utils import common_texts
import joblib
# from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pandas as pd

model = hub.load("C:/Users/Vijay Jonathan/Downloads/Compressed/universal-sentence-encoder-large_5")

# ========================================================#

import pandas as pd
# import warnings 
# import gensim 
# Reader class does reading file operations for you 
# Please specify a correct path to the file 
class reader:
  # This function reads original FAQ file and returns questions and answers 
  # Return type : questions - list of strings, answers - list of dataframes (to be compatible with tabular data) 
  # test and train are kept False , if you want train or test data other than FAQ data ,opt True accordingly
  # if you want to read the file containing abbreviations opt for abbr = True this returns abbreviations and full forms respectively
  def read_excel(self,filename,train=False,test=False,abbr=False):
    if train == False and test == False and abbr == False:
      # Read the contents of excel file into a dataframe
      # default index and header values are 0 but you change according to your excel file 
      df = pd.read_excel(filename) 
      questions = list() 
      answers = list() 
      # iterate throught the dataframe 
      for i in range(len(df)):
        # check whether df.iloc[i,0] i.e., question is a string or not. 
        if type(df.iloc[i,0]) == str:
          questions.append(df.iloc[i,0])
          answers.append(df.iloc[i,1])
      return questions,answers

    else:
      # read the contents of training file into a dataframe 
      # default index and header values are 0 but you change according to your excel file 
      df = pd.read_excel(filename)
      x = list()
      y = list()
      for i in range(len(df)):
        x.append(df.iloc[i,1])
        y.append(df.iloc[i,0])
      if abbr:
        return y,x
      
      return x,y

# ==================================================================================================
import pandas as pd
# import csv
import re
#from read import reader 
# This class helps preprocessing steps like removing punctuations,abbreviations etc.
class remover:
    def __init__(self,filename):
        obj = reader()
        self.abbr, self.full = obj.read_excel(filename,abbr=True)
        # By default this function removes abbreviations from each sentence in a list of sentences 
        # If removing punctuations also needed to be removed opt for True 
        # If you want to keep abbreviations as it is and remove punctuations then put abbr=False 
    def preprocess(self,sentence,abbr=True,punct=True):
        sentence = re.sub("\n"," ",sentence)
        sentence = sentence.strip()
        if punct:
            punctuations = '''!()-[]{};:"\,<>./?@#$%^&*_—'''
            no_punct = ""
            for char in sentence:
                if char not in punctuations:
                    no_punct = no_punct + char
                else:
                    no_punct += " "
            sentence = no_punct

        if abbr:
            temp = list()
            tokens = sentence.split(" ")
            for token in tokens:
                if token.lower() in self.abbr:
                    temp.append(self.full[self.abbr.index(token.lower())])
                else:
                    temp.append(token)
                    sentence = " ".join(temp)

        return sentence 
# =================================================================================================
# This is for USE

import pandas as pd
import numpy as np
# from gensim.models.doc2vec import Doc2Vec, TaggedDocument
# from gensim.utils import simple_preprocess
#from read import reader
#from remove import remover
import joblib
# import gensim
from sklearn.metrics.pairwise import cosine_similarity

# Get similar question number as the asked query
def get_sim(query,question):
    temp = list()
    # thresh_correct = 0.7
    # thresh_diff = 0.02
    for x in question:
        arr = cosine_similarity(query,[x])
        temp.append(arr[0][0])
    # if np.max(temp) < thresh_correct:
    #     return -1
    res = np.array(temp)
    # res = np.sort(res)
    # res = np.flipud(res)
    # if res[0]-res[1] < thresh_diff:
    #     return [temp.index(res[0]),temp.index(res[1])]
    return np.argmax(temp)

# To get accuracy
def get_accuracy(sims,y_test):
    count = 0
    for i in range(len(sims)):
        if sims[i] == y_test[i]:
            count += 1
    return count/len(sims)




# =====================================================================================
def use(query):
    # load the saved model
    # model = hub.load("https://tfhub.dev/google/universal-sentence-encoder-large/5")
    # model = hub.load("C:/Users/Vijay Jonathan/Documents/GitHub/StudentBuddyPortal/universal-sentence-encoder-large_5")
    # reader object
    read = reader()
    # remover object
    Acc=0.8251
    remove = remover("Abbr.xlsx")
    # read questions and answers
    filename = "faq3.xlsx"
    questions , answers = read.read_excel(filename)
    temp = list()
    for question in questions:
        temp.append(remove.preprocess(question,punct=True))
    questions = temp
    # print(questions,answers)
    # get embeddings for questions
    questions_embeds = np.array(model(questions))
    # print(questions_embeds.shape)
    #test file path
    # test_file = "NEWAV3.xlsx"
    # x_test,y_test = read.read_excel(test_file,test=True)
    # temp = list()
    # for x in x_test:
    #     temp.append(remove.preprocess(x,punct=True))
    # x_test = temp
    # # print(x_test)
    # test_embeds = np.array(model(x_test))
    # sims = list()
    # for test in test_embeds:
    #     sims.append(get_sim([test],questions_embeds))
    # acc = get_accuracy(sims,y_test)
    # print("Accuracy = ", Acc*100)
    # model.save('my_model.h1')

    # joblib.dump(model,"use.pkl")
    # tf.saved_model.save(model, "use.h1")

    # query = input("Enter your query : ")
    
    query = remove.preprocess(query,punct=True)
    query_embeds = np.array(model([query]))
    # generate similarity
    sims = get_sim(query_embeds,questions_embeds)
    if sims != -1 and type(sims)!=list:
        r = answers[sims]
        # print(answers[sims])
        return r


    # while True:
    #     # take input query
    #     query = input("Enter your query : ")
    #     if query == "bye":
    #         return
    #     query = remove.preprocess(query,punct=True)
    #     query_embeds = np.array(model([query]))
    #     # generate similarity
    #     sims = get_sim(query_embeds,questions_embeds)
    #     if sims != -1 and type(sims)!=list:
    #         print(answers[sims])

# ================================================================================










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
        query = request.form['query']
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
        # op ="Click on this ink to open AUMS https://intranet.cb.amrita.edu/aums"
        op = use(query)
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

