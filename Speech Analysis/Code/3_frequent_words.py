#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 16:28:23 2017

@author: archit
"""
import nltk

def get_most_frequent(speaker, stemmer, n):
    filename = speaker + "_" + stemmer + ".txt"
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.readline()
        stems = data.split(" ")
        
        mc = nltk.FreqDist(stems).most_common(n)
        mf = [pair[0] for pair in mc]
        
        return mf
    
    
speakers = ["Romney", "Obama", "Lehrer"]
stemmers = ["porter", "lancaster", "snowball"]

n = 10

for speaker in speakers:
    for stemmer in stemmers:
        l = get_most_frequent(speaker, stemmer, n)
        print(speaker, stemmer)
        print(l, "\n")
