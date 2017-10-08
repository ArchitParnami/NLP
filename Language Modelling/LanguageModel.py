#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 10:11:39 2017

@author: archit
"""

import nltk
from nltk.corpus import udhr
from nltk.util import ngrams
import string

#calulate probabilty distribution from frequency distribution
def compute_pdf(fdist):
    total = 0
    for key in fdist:
        total = total + fdist[key]
    pdf = {}
    for key in fdist:
        pdf[key] = fdist[key]/total
    return pdf

#remove punctuations
def remove_punc(text):
    new_text = []
    for ch in text:
        if ch not in string.punctuation:
            new_text.append(ch)
    
    return ''.join(new_text)
    
# removes punctuations, converts to lower case and substitute new lines and
# spaces with '_'
def preprocess(text):
    text = text.strip()
    text = remove_punc(text)
    text = str.lower(text)
    text = text.replace('\n', '_')
    text = text.replace(' ', '_')
    
    if text=='':
        text="_"
    
    return text

ENGLISH = 0
FRENCH = 1
ITALIAN = 2
SPANISH = 3

LANGUAGES = [ENGLISH, FRENCH, ITALIAN, SPANISH]
LANG_NAMES = ["English", "French", "Italian", "Spanish"]

english = udhr.raw('English-Latin1') 
french = udhr.raw('French_Francais-Latin1') 
italian = udhr.raw('Italian_Italiano-Latin1') 
spanish = udhr.raw('Spanish_Espanol-Latin1')  

data = [preprocess(lang) for lang in [english, french, italian, spanish]]

english = data[ENGLISH]
french = data[FRENCH]
italian = data[ITALIAN]
spanish = data[SPANISH]

#train data for all languages
train = [english[0:1000],french[0:1000],
         italian[0:1000],spanish[0:1000]]

dev = [english[1000:1100], french[1000:1100],
       italian[1000:1100],spanish[1000:1100]]

test = [udhr.words('English-Latin1')[0:1000],
        udhr.words('French_Francais-Latin1')[0:1000],
        udhr.words('Italian_Italiano-Latin1')[0:1000], 
        udhr.words('Spanish_Espanol-Latin1')[0:1000]]

#preprocess test data as well
test = [[preprocess(word) for word in test_set] for test_set in test]


#ngram models computed with nltk.util.ngrams

Unigrams = [ngrams(train[LANGUAGE], 1) 
            for LANGUAGE in LANGUAGES]

Bigrams = [ngrams(train[LANGUAGE], 2, 
                  pad_left=True, pad_right=True, 
                  left_pad_symbol='_', right_pad_symbol='_') 
            for LANGUAGE in LANGUAGES]

Trigrams = [ngrams(train[LANGUAGE], 3, 
                  pad_left=True, pad_right=True, 
                  left_pad_symbol='_', right_pad_symbol='_') 
            for LANGUAGE in LANGUAGES]
 

#frequency distribution of N-Grams
freq_Uni = [nltk.FreqDist(unigram) for unigram in Unigrams]
freq_Bi = [nltk.FreqDist(bigram) for bigram in Bigrams]
freq_Tri = [nltk.FreqDist(trigram) for trigram in Trigrams]

# probability distribution of N-Grams
prob_Uni = [compute_pdf(fdist) for fdist in freq_Uni]
prob_Bi = [compute_pdf(fdist) for fdist in freq_Bi]
prob_Tri = [compute_pdf(fdist) for fdist in freq_Tri]


#given a word, calulate its unigram model probabilty for given LANGUAGE 
def compute_unigram_probability(word, LANGUAGE):
    p = 1
    dr = prob_Uni[LANGUAGE]
    for ch in word:
        key = (ch,)
        p_key = dr[key] if key in dr else 0
        
        if p_key == 0:
            return 0
        
        p = p * p_key
        
    return p

#given a word, calulate its bigram model probabilty for given LANGUAGE 
def compute_bigram_probabilty(word, LANGUAGE):
    L = len(word)
    
    if L < 2:
        return compute_unigram_probability(word, LANGUAGE)
    
    p = 1
    dr = prob_Bi[LANGUAGE]
    
    for i in range(L+1):
        if i == 0:
            key = ('_',word[i])
        elif i == L:
            key == (word[i-1], '_')
        else:
            key = (word[i-1],word[i])
        
        p_key = dr[key] if key in dr else 0
        
        if p_key == 0:
            return 0
        
        prev = '_' if i == 0 else word[i-1]
        
        p = p * p_key / compute_unigram_probability(str(prev), LANGUAGE)
    
    return p;

#given a word, calulate its trigram model probabilty for given LANGUAGE 
def compute_trigram_probability(word, LANGUAGE):
    L = len(word)
    if L < 3:
        return compute_bigram_probabilty(word, LANGUAGE)
    
    p = 1
    dr = prob_Tri[LANGUAGE]
    
    for i in range(1, L+1):
        if i == 1:
            key = ('_', word[i-1], word[i])
        elif i == L:
            key = (word[i-2], word[i-1], '_')
        else:
            key = (word[i-2], word[i-1], word[i])
        
        p_key = dr[key] if key in dr else 0
        
        if p_key == 0:
            return 0
        
        key2 = ('_', word[i-1]) if i == 1 else (word[i-2], word[i-1])
        p_key2 = prob_Bi[LANGUAGE][key2]
        
        p = p * p_key / p_key2
    
    return p


#given a word, calculate N-Gram model accuracy  for language LANG_!
def predict_language(test_set, LANG_1, LANG_2):
    
    n = len(test_set)
    
    filename = LANG_NAMES[LANG_1] + "_" + LANG_NAMES[LANG_2] +"_" + str(n) + ".txt"
    
    uni_matches = 0
    bi_matches = 0
    tri_matches = 0
    
    with open(filename, 'w') as f:
       
        lang_pair = "({0}, {1})\n\n".format(LANG_NAMES[LANG_1], LANG_NAMES[LANG_2])
        f.write(lang_pair)
       
        header = "{0:15s}{1:37s}\t{2:37s}\t{3:37s}\n".format("WORD", "UNIGRAM", "BIGRAM", "TRIGRAM")
        f.write(header)
       
        for word in test_set:
            p1 = compute_unigram_probability(word, LANG_1)
            p2 = compute_unigram_probability(word, LANG_2)
        
            p3 = compute_bigram_probabilty(word, LANG_1)
            p4 = compute_bigram_probabilty(word, LANG_2)
        
            p5 = compute_trigram_probability(word, LANG_1)
            p6 = compute_trigram_probability(word, LANG_2)
    
            if p1 >= p2:
                uni_matches = uni_matches + 1
        
            if p3 >= p4:
                bi_matches = bi_matches + 1
        
            if p5 >= p6:
                tri_matches = tri_matches + 1


            prob = "{0:15s}({1:.15f},{2:.15f})\t({3:.15f},{4:.15f})\t({5:.15f},{6:.15f})\n".format(word,p1,p2,p3,p4,p5,p6)
            f.write(prob);
            
    
    uni_prob = uni_matches * 100 / n
    bi_prob =  bi_matches * 100 / n
    tri_prob = tri_matches * 100 / n
    
    border = "*"  * 60
    print(border)
    print("N-Gram Model Accuracy that language is: " + LANG_NAMES[LANG_1] + "\n")
    print("Unigram: = {0:.3f}".format(uni_prob))
    print("Bigram: = {0:.3f}".format(bi_prob))
    print("Trigram: = {0:.3f}".format(tri_prob))   
    print("\nWord probabilities written to file " + filename+"\n")
    

print("\nDEV SETS:\n")
predict_language(dev[ENGLISH].split('_'), ENGLISH, FRENCH);
predict_language(dev[SPANISH].split('_'), SPANISH, ITALIAN);

print("TEST SETS:\n")
#Question 1
predict_language(test[ENGLISH], ENGLISH, FRENCH);
#Question 2
predict_language(test[SPANISH], SPANISH, ITALIAN);
