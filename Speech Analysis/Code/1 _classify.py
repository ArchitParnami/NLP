#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 10:54:05 2017

@author: archit
"""
import re

expr = '\([^)]*\)';

R = "ROMNEY:"
O = "OBAMA:"
L = "LEHRER:"

ROMNEY = ""
OBAMA = ""
LEHRER = ""

R_SPEAKS = False
O_SPEAKS = False
L_SPEAKS = False

with open('debate.txt', 'r', encoding='utf-8') as debate:
    for line in debate:
        line = re.sub(expr, "", line).strip()
        if line == "":
            continue;
        
        if line.startswith(R) or line.startswith(O) or line.startswith(L):
           
            R_SPEAKS = False
            O_SPEAKS = False
            L_SPEAKS = False
            
            if line.startswith(R):
                statement = line[len(R):].strip()
                ROMNEY  = ROMNEY + statement + " "
                R_SPEAKS = True
            
            elif line.startswith(O):
                statement = line[len(O):].strip()
                OBAMA  = OBAMA + statement + " "
                O_SPEAKS = True
            
            else:
                statement = line[len(L):].strip()
                LEHRER = LEHRER + statement + " "
                L_SPEAKS = True
            
        else:
            
            if R_SPEAKS:
                ROMNEY  = ROMNEY + line + " "
            elif O_SPEAKS:
                OBAMA  = OBAMA + line + " "
            elif L_SPEAKS:
                if not line.startswith("©"): # skip this line
                    LEHRER = LEHRER + line + " "
            else:
                continue;

with open('Romney.txt','w', encoding='utf-8') as romney:
    romney.write(ROMNEY)

with open('Obama.txt','w', encoding='utf-8') as obama:
    obama.write(OBAMA)

with open('Lehrer.txt','w', encoding='utf-8') as lehrer:
    lehrer.write(LEHRER)
