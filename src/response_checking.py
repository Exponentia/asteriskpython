# -*- coding: utf-8 -*-
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import datefinder
import re
import datetime
import sys
x = datetime.datetime(1986, 8, 31)
#print sys.argv[1]
def intent_recog(text):
    pass
def agree(text):
    print text,"@"*20
    if text:
        positive_answer_text = ["Yes","i agree","yes thanks you","sure","yes please","ok"]
        negative_answer_text = ["not","No","I am not sure","no, i didn't agree for this"]
        positive =[]
        negative =[]
        print process.extract(text, positive_answer_text)
        for i in process.extract(text, positive_answer_text):
            positive.append(i[1])
        for i in process.extract(text, negative_answer_text):
            negative.append(i[1])
        pos = max(positive)
        neg = max(negative)
        print neg
        print pos
        if pos>50 or neg >50:
            if pos>neg:
                return "1"
            else:
                return "2"
    return "0"
def text_got(text):
    print text,"@"*20
    if text:
        positive_answer_text = ["speaking","Yes","yes this is","this is","you are speaking to","yes please","ok"]
        negative_answer_text = ["he is not available","No","I am not sure","this is not him","he is not available"]
        positive =[]
        negative =[]
        print process.extract(text, positive_answer_text)
        for i in process.extract(text, positive_answer_text):
            positive.append(i[1])
        for i in process.extract(text, negative_answer_text):
            negative.append(i[1])
        pos = max(positive)
        neg = max(negative)
        print neg
        print pos
        if pos>50 or neg >50:
            if pos>neg:
                return "1"
            else:
                return "2"
    return "0"
#print text_got("yes this is uncle jesse")
import datetime
def dob(text):
    global x
    matches = datefinder.find_dates(text)
    matches = list(matches)
    print matches
    if len(matches)>=1:
        if matches[0].strftime("%d") == x.strftime("%d") and matches[0].strftime("%B") == x.strftime("%B") and matches[0].strftime("%Y") == x.strftime("%Y"):
            return "1"
        elif matches[0].strftime("%d") == x.strftime("%d") and matches[0].strftime("%B") == x.strftime("%B") and matches[0].strftime("%Y") != x.strftime("%Y"):
            return "2"
        elif matches[0].strftime("%d") == x.strftime("%d") and matches[0].strftime("%B") != x.strftime("%B") and matches[0].strftime("%Y") == x.strftime("%Y"):
            return "3"

        else:
            return "0"
#    if fuzz.ratio(text," august 1986") >10:
#        return "1"
#    else:
#        return "0"
#print dob("i was born on 31st october 1986")
def take_dob_month(text): 
    global x
    print x.strftime("%B").lower
    if x.strftime("%B").lower() in text:
        print fuzz.ratio(text,x.strftime("%B"))
#    if fuzz.ratio(text,x.strftime("%B")) > 70:    
        return "1"
    else:
        return "0"

def take_dob_year(text):
    global x
    print type(x.strftime("%Y"))
    digits_string = re.findall(r'\b\d+\b', text)
    print digits_string
    for i in digits_string:
#        print (i)==(x.strftime("%Y"))
#        print (x.strftime("%Y"))
        if len(i)==4:
            print i == x.strftime("%Y")
            if i == x.strftime("%Y"):
                return "1"
    return "0"

#print take_dob_year("1986")
import re
def phonenumber(text):
    d= re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
    print d,"phone number"
    if len(d)>0:
        if fuzz.ratio(d[0],"992-048-2274") >80:
            return "1"
        else:
            return "0"
print phonenumber("My phone number is 992-048-2274")
def email(text):
    phonetics=["Alpha","Bravo","Charlie","Delta","Echo","Foxtrot","Golf","Hotel","India","Juliet","Kilo","Lima","Mike","November","Oscar","Papa","Quebec","Romeo","Sierra","Tango","Uniform","Victor","Whiskey","X-ray","Yankee","Zulu"]
    new_text=text.split(" ")
    print new_text
    ver_phonetics = ['India','November','Foxtrot','Oscar','AT','gmail']
    j=0
    for i in new_text:
        print process.extractOne(i, ver_phonetics)
        if process.extractOne(i, ver_phonetics)[1]== 100:
            j = j+1
            if i >=3:
                return "1"
        else:
            return "0"
#print type(dob("31sut"))
        
email("india november foxtrot oscar at gmail.com")