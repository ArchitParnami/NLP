#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 17:49:42 2017

@author: archit
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 17:25:03 2017

@author: archit
"""

#import matplotlib.pyplot as plt

def get_positive_stem_rate(speaker):
    filename = speaker + "_porter.txt"
    
    with open(filename, 'r', encoding='utf8') as f:
        data = f.readline()
    
    stems = data.split(' ')
    
    with open('positive_stems.txt', 'r', encoding='utf-8') as pf:
        data = pf.readline()
    
    pstems = data.split(' ')
    
    X = []
    Y = []
    w = 0
    p = 0
    
    for stem in stems:
        w = w+1
        X.append(w)
        if stem in pstems:
            p = p + 1
        Y.append(p)
    
    
    t = len(X)
    rate_file = speaker + '_rate.txt'
    
    with open(rate_file, 'w', encoding='utf-8') as rf:
        for i in range(t):
            #line = str(X[i]) + "\t" + str(Y[i]) + "\n"
            line = "%d\t%d\n" % (X[i], Y[i])
            rf.write(line)
        

get_positive_stem_rate("Romney")
get_positive_stem_rate("Obama")
get_positive_stem_rate("Lehrer")