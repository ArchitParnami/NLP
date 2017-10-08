#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 16:47:09 2017

@author: archit
"""

import nltk

def stem_positive_words():
    with open('positive.txt', 'r', encoding='utf-8') as pf:
        lines = pf.readlines()
    
    words = [line.strip() for line in lines]
    porter = nltk.PorterStemmer()
    stems = [porter.stem(word) for word in words]
    
    stems = set(stems)
    
    data = " ".join(stems)
    outfile = 'positive_stems.txt'
    
    
    with open(outfile, 'w', encoding='utf-8') as pfs:
        pfs.write(data)
    
    print("output written to " + outfile)

      
stem_positive_words()