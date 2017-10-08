#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 17:01:56 2017

@author: archit
"""

import nltk

def get_most_frequent_positives(speaker, n):
     filename = speaker + "_porter.txt"
     positive_file = 'positive_stems.txt'
     
     with open(filename, 'r', encoding='utf-8') as sf:
         data = sf.readline()
         stems = data.split(' ')
     
     with open(positive_file, 'r', encoding='utf-8') as pf:
        data = pf.readline()
        positive_stems = data.split(' ')
      
     speaker_positive_stems = []  
     
     for stem in stems:
        if stem in positive_stems:
            speaker_positive_stems.append(stem)
    
     total_positives = len(speaker_positive_stems)
     fDist = nltk.FreqDist(speaker_positive_stems)
     freq_positives = [pair[0] for pair in fDist.most_common(n)]
     return (total_positives, freq_positives)
 
    

speakers = ["Romney", "Obama", "Lehrer"]
most_positive = -1
positive_speaker = ""

for speaker in speakers:
    (total_positives, freq_positives) = get_most_frequent_positives(speaker, 10)
    print(speaker, total_positives)
    print(freq_positives, "\n")
    if total_positives > most_positive:
        most_positive = total_positives
        positive_speaker = speaker

print(positive_speaker + " speaks positive words most often.")
    