#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 13:54:16 2017

@author: archit
"""

import string
import nltk
from nltk.corpus import stopwords


def find_stems(speaker):

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
        
        tokens = nltk.word_tokenize(text);
        
        porter = nltk.PorterStemmer()
        lancaster = nltk.LancasterStemmer()
        snowball = nltk.SnowballStemmer("english")
        
        porter_stems = []
        lancaster_stems = []
        snowball_stems = []
        
        for word in tokens:
            porter_stems.append(porter.stem(word))
            lancaster_stems.append(lancaster.stem(word))
            snowball_stems.append(snowball.stem(word))
        
        outfile = filename.strip(".txt");
        porter_file = outfile + "_porter.txt"
        lancaster_file = outfile + "_lancaster.txt"
        snowball_file = outfile + "_snowball.txt"
        
        with open(porter_file, 'w', encoding='utf-8') as pf:
            data = " ".join(porter_stems)
            pf.write(data)
            print("Stems written to file " + porter_file)
         
        with open(lancaster_file, 'w', encoding='utf-8') as lf:
            data = " ".join(lancaster_stems)
            lf.write(data)
            print("Stems written to file " + lancaster_file)
        
        with open(snowball_file, 'w', encoding='utf-8') as sf:
            data = " ".join(snowball_stems)
            sf.write(data)
            print("Stems written to file " + snowball_file)



speakers = ["Romney", "Obama", "Lehrer"]

for speaker in speakers:  
    find_stems(speaker)
    



