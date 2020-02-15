# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 13:17:04 2019

@author: Ameer Hamza
"""
import csv
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


dataSet=[]
Words={}
totalPos=0.0
totalNag=0.0
TestSet=[]

with open("TraningData.csv") as file:
    read = csv.reader(file)
    for row in read:
        tempList=[]
        if(row[0]!= "class"):
            tempList.append(row[0])
            tempList.append(row[1])
            dataSet.append(tempList)

for data in dataSet:
    example_sent = data[1].lower()
    stop_words = set(stopwords.words('english'))
    example_sent=re.sub(r'[^\w\s]','',example_sent)
    example_sent=''.join([i for i in example_sent if not i.isdigit()])
    word_tokens = example_sent.split(" ")
    filtered_sentence = word_tokens
    for word in filtered_sentence:
        if word not in Words:
            Words[word]=[0.0,0.0,0.0,0.0]
            print(word)
        if (data[0]=="Pos"):
            Words[word][0]=Words[word][0]+1
            totalPos=totalPos+1;
        else:
            Words[word][1]=Words[word][1]+1
            totalNag=totalNag+1

for i in Words:
    Words[i][2]=Words[i][0]/totalPos
    Words[i][3]=Words[i][1]/totalNag

with open("Test.csv") as file:
    read = csv.reader(file)
    for row in read:
        tempList=[]
        if(row[0]!= "class"):
            tempList.append(row[0])
            tempList.append(row[1])
            TestSet.append(tempList)
hits=0.0  
countPos=0.0
countNeg=0.0
for string in TestSet:
    products=[1,1]
    tempStr=string[1].lower()
    test = tempStr.split(" ")
    for word in test:
        if word in Words:
            if ((products[0]*(Words[word][2]*100))<=0.0) or ((products[1]*(Words[word][3]*100))<=0.0):
                products[0]=products[0]*1000
                products[1]=products[1]*1000
            if Words[word][2]!=0:
                products[0]=products[0]*(Words[word][2]*100)
            if Words[word][3]!=0:
                products[1]=products[1]*(Words[word][3]*100)
    if products[0] > products[1]:
        countPos=countPos+1
        print(products,"pos",string[0])
        if (string[0]=="Pos"):
            hits=hits+1
    else:
        countNeg=countNeg+1
        print(products,"Neg",string[0])
        if (string[0]=="Neg"):
            hits=hits+1
        
print((countPos/200)*100)
print((countNeg/200)*100)
print((hits/(400))*100)