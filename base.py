#!/usr/bin/env python3
"""
Search engine for Library of Words.

Type base.py -h from terminal for usage.

TODO: clean code
      optimize (use dictionary?)
"""

import random
import re
import argparse

__author__ = 'Giulio Pepe'
__email__ = 'wordlibrarian@gmail.com'
__date__ = "Nov 25, 2015"

parser = argparse.ArgumentParser(description='Base engine for libraryofwords.info. Usage:')
parser.add_argument('-t', '--looktext', type=str, help='Look for text in the library and return location')
parser.add_argument('-p', '--lookpage', type=str, help='Look for a location in the library and return text')
parser.add_argument('-s', '--stringonly', action='store_true', help='String only mode on')
args = parser.parse_args()
 
# Open vocabulary
vocabwords = []
base62 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
nofwords = 0
wordsinpage = 320
with open("vocab.txt") as word_file:
    for line in word_file:
        vocabwords.append(line.rstrip('\r\n'))        
        nofwords += 1
        
# Generalized-base encoder -> gives words from page number
# Also used for base62 encoding
def base_encode(page, words=vocabwords):
    if (page == 0):
        return words[0]
    arr = []
    base = len(words)
    while page:
        rem = page % base
        page = page // base
        arr.append(words[rem])
    arr.reverse()
    return ' '.join(arr)

# Generalized-base decoder -> gives page number from text (if word not in vocab, ignore)
# Also used for base62 decoding
def base_decode(text, words=vocabwords, vocabulary=True):
    if vocabulary: # check if words in vocabulary 
        newtext = []
        text = re.sub(r'\W+', ' ', text) # remove unknown chars
        splittext = text.split()
        c = 0
        while c < wordsinpage: # with limit to 320 words
            try:
                currentword = splittext[c]
                if currentword.isdigit():
                    numberword = numToWords(int(currentword))
                    for i in numberword.split():
                        newtext.append(i)
                        c += 1
                elif currentword in words:
                    newtext.append(text.split()[c])
                c += 1
            except IndexError:
                break
        text = newtext
    base = len(words)
    strlen = len(text)
    page = 0
    idx = 0
    for word in text:
        try:
            power = (strlen - (idx + 1))
            page += words.index(word) * (base ** power)
            idx += 1
        except ValueError:
            print('Error in the vocab')
            pass
    return ' '.join(text), page

# Transforms integers to words
def numToWords(num,join=True):
    '''words = {} convert an integer number into words'''
    units = ['','one','two','three','four','five','six','seven','eight','nine']
    teens = ['','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
    tens = ['','ten','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
    thousands = ['','thousand','million','billion','trillion','quadrillion','quintillion','sextillion','septillion','octillion','nonillion','decillion','undecillion','duodecillion','tredecillion','quattuordecillion','sexdecillion','septendecillion','octodecillion','novemdecillion','vigintillion']
    words = []
    if num==0: words.append('zero')
    elif num>999999999999999999999999999999999999999999999999999999999999999: words.append('infinite')
    else:
        numStr = '%d'%num
        numStrLen = len(numStr)
        groups = (numStrLen+2)//3
        numStr = numStr.zfill(groups*3)
        for i in range(0,groups*3,3):
            h,t,u = int(numStr[i]),int(numStr[i+1]),int(numStr[i+2])
            g = groups-(i//3+1)
            if h>=1:
                words.append(units[h])
                words.append('hundred')
            if t>1:
                words.append(tens[t])
                if u>=1: words.append(units[u])
            elif t==1:
                if u>=1: words.append(teens[u])
                else: words.append(tens[t])
            else:
                if u>=1: words.append(units[u])
            if (g>=1) and ((h+t+u)>0): words.append(thousands[g])
    if join: return ' '.join(words)
    return words

# Creates random page for the searched string
def genfullpage(textofpage, words=vocabwords):
    fullpage = textofpage.split()
    wordsinstring = len(textofpage.split())
    start=random.randrange(0,wordsinpage-wordsinstring)
    end=wordsinstring+start
    for i in range(0,start): 
        fullpage.insert(0,words[random.randrange(0,nofwords-1)])
    for i in range(end,wordsinpage):
        fullpage.append(words[random.randrange(0,nofwords-1)])
    location = base_encode(base_decode(' '.join(fullpage))[1],base62)
    return start, end, fullpage, location

## Deprecated
## forward LCG
## https://en.wikipedia.org/wiki/Linear_congruential_generator
## m,a,c satisfy Hull-Dobell theorem to ensure no repetitions
#def nextv(seed):
#    m = nofwords**wordsinpage
#    a = nofwords**(wordsinpage-20+1)
#    c = 136481**(wordsinpage-20)
#    randomized = ( a * seed + c ) % m
#    return randomized

## Deprecated
## reverse LCG implementing Euclid's algo
#def prevv(seed):
#    m = nofwords**wordsinpage
#    a = nofwords**(wordsinpage-20+1)
#    c = 136481**(wordsinpage-20)
#    qarray = [0,0,0,0,0,0,0,0,0,0,0,0]
#    qarray[0] = 0
#    qarray[1] = 1
#    i = 2
#    reset = m
#    while m % a > 0:
#        remainder = m % a
#        quotient = m / a
#        #print m,a
#        qarray[i] = qarray[i-2]-(qarray[i-1] * quotient)
#        m = a
#        a = remainder
#        i += 1
#
#    if qarray[i-1] < 0:
#        qarray[i-1]+=reset
#
#    randomized = ( (seed - c) * qarray[i-1] ) % m
#    return randomized

    
# Text -> Location string
if args.looktext:
    text = args.looktext
    text,page = base_decode(''.join(text))
    if not args.stringonly and len(text.split()) < 320:
        s,s,text,location = genfullpage(text)
        print('"',' '.join(text),'"',sep='')
        print(location.replace(' ',''))
    else:
        print('"',text,'"',sep='')
        print(base_encode(page,base62).replace(' ',''))

# Location string -> Text
if args.lookpage:    
    location,page = base_decode(args.lookpage,base62,False)
    text = base_encode(page)
    if not args.stringonly and len(text.split()) < 320:
        s,s,text,location = genfullpage(text)
        print('"',' '.join(text),'"',sep='')
        print(location.replace(' ',''))
    else:
        print('"',base_encode(page),'"',sep='')
        print(location.replace(' ',''))


