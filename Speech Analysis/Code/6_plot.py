#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 17:25:03 2017

@author: archit
"""

import string
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

def plot_positive_word_rate(speaker):
    filename = speaker + ".txt"
    
    with open(filename, 'r', encoding='utf8') as f:
        text = f.readline()
        
    NO_PUN = ""
    for ch in text:
        if ch not in string.punctuation:
            NO_PUN = NO_PUN + ch
    
    text = NO_PUN.lower()
    
    words = text.split()
    stop_words = stopwords.words('english')
    stop_words.extend(["im", "thats"])
    
    text_words = []
    
    for word in words:
        if word not in stop_words:
            text_words.append(word)
    
    text = ' '.join(text_words)
    tokens = nltk.word_tokenize(text)
    
    with open('positive.txt', 'r', encoding='utf-8') as pf:
        lines = pf.readlines()
    pwords = [line.strip() for line in lines]
    
    X = []
    Y = []
    w = 0
    p = 0
    for word in tokens:
        w = w+1
        X.append(w)
        if word in pwords:
            p = p + 1
        Y.append(p)
    
    plt.plot(X, Y)
    

plot_positive_word_rate("Romney")
plot_positive_word_rate("Obama")
plot_positive_word_rate("Lehrer")