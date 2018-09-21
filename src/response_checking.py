# -*- coding: utf-8 -*-
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import datefinder

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
        positive_answer_text = ["Yes","yes this is","this is","you are speaking to","yes please","ok"]
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
print text_got("No")

def dob(text):
    matches = datefinder.find_dates(text)
    
    if fuzz.ratio(text,"31st august 1986") >10:
        return "1"
    else:
        return "0"
def phonenumber(text):
    print text,"phone number"
    if fuzz.ratio(text,"992-048-2274") >80:
        return "1"
    else:
        return "0"
def email(text):
    if fuzz.ratio(text,"ankur@gmail.com") >50:
        return "1"
    else:
        return "0"
print type(dob("31sut"))