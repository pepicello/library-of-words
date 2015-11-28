#!/usr/bin/env python3
"""
Search engine for Library of Words.

Type base.py -h from terminal for usage.
"""

import random
import re
import argparse

__author__ = 'Giulio Pepe'
__email__ = 'wordlibrarian@gmail.com'

parser = argparse.ArgumentParser(description='Base engine for libraryofwords.info. Usage:')
parser.add_argument('-t', '--looktext', type=str, help='Look for text in the library and return location')
parser.add_argument('-p', '--lookpage', type=str, help='Look for a location in the library and return text')
parser.add_argument('-s', '--stringonly', action='store_true', help='String only mode on')
args = parser.parse_args()
 
# Open vocabulary
vocabwords = {}
base62 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
nofwords = 0
wordsinpage = 320
with open("vocab.txt") as word_file:
    for key,value in enumerate(word_file):
        vocabwords[value.rstrip('\r\n')] = key
        nofwords += 1
inversevocab = {v: k for k, v in vocabwords.items()}

# Clean text input
def text_cleaner(text):
    modtext = []
    text = re.sub(r'\W+', ' ', text) # remove unknown chars
    splittext = text.split()
    c = 0
    while c < wordsinpage: # with limit to 320 words
        try:
            currentword = splittext[c]
            if currentword.isdigit():
                numberword = numToWords(int(currentword))
                for i in numberword.split():
                    modtext.append(i)
                    c += 1
            elif currentword in vocabwords:
                modtext.append(text.split()[c])
            c += 1
        except IndexError:
            break
    return modtext

# Generalized-base encoder -> gives words from page number
# Also used for base62 encoding
def base_encode(page):
    if (page == 0):
        return 'a'
    arr = []
    while page:
        rem = page % nofwords
        page = page // nofwords
        arr.append(inversevocab[rem])
    arr.reverse()
    return ' '.join(arr)

# Generalized-base decoder -> gives page number from text (if word not in vocab, ignore)
# Also used for base62 decoding
def base_decode(text):
    modtext = text_cleaner(text)
    strlen = len(modtext)
    page = 0
    idx = 0
    if strlen == 0:
        return '', -1
    for word in modtext:
        try:
            power = (strlen - (idx + 1))
            page += vocabwords[word] * (nofwords ** power)
            idx += 1
        except ValueError:
            print('Error in the vocab. Possibly missing word')
            pass
    return ' '.join(modtext), page

def base62_encode(decimal):
    if (decimal == 0):
        return base62[0]
    arr = []
    base = len(base62)
    while decimal:
        rem = decimal % base
        decimal = decimal // base
        arr.append(base62[rem])
    arr.reverse()
    return ''.join(arr)

def base62_decode(base62number):
    base = len(base62)
    strlen = len(base62number)
    decimal = 0
    idx = 0
    for word in base62number:
        power = (strlen - (idx + 1))
        decimal += base62.index(word) * (base ** power)
        idx += 1
    return decimal
    
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
def genfullpage(text):
    fullpage = text_cleaner(text)
    wordsinstring = len(fullpage)
    if wordsinpage == wordsinstring:
        start=0
    else:
        start=random.randrange(0,wordsinpage-wordsinstring)
    end=wordsinstring+start
    for i in range(0,start): 
        fullpage.insert(0,inversevocab[random.randrange(0,nofwords-1)])
    for i in range(end,wordsinpage):
        fullpage.append(inversevocab[random.randrange(0,nofwords-1)])
    location = base62_encode(base_decode(' '.join(fullpage))[1])
    return start, end, fullpage, location



    
# Text -> Location string
if args.looktext:
    text = args.looktext
    text,page = base_decode(''.join(text))
    if not args.stringonly:
        s,s,text,location = genfullpage(text)
        print('"',' '.join(text),'"',sep='')
        print(location)
    else:
        if page == -1:
            print('ERROR: All words missing from vocabulary')
        else:
            print('"',text,'"',sep='')
            print(base62_encode(page))

# Location string -> Text
if args.lookpage:    
    page = base62_decode(args.lookpage)
    text = base_encode(page)
    if not args.stringonly:
        s,s,text,location = genfullpage(text)
        print('"',' '.join(text),'"',sep='')
        print(location)
    else:
        if page == -1:
            print('ERROR: All words missing from vocabulary')
        else:
            print('"',base_encode(page),'"',sep='')
            print(args.lookpage)

