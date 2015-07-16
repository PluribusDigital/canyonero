## Imports

import os
import csv
import nltk
import json
import math
import random
import distance 

## Important Paths
DATAPATH = os.path.join(os.path.dirname(__file__), "../../data/")

def load_data(name):
    """
    Create a generator to load data from the data source.
    """
    with open(os.path.join(DATAPATH, name), 'r') as f:
        reader = csv.DictReader(f, dialect='excel-tab')
        for row in reader:
            yield row['name']

lemmatizer = nltk.WordNetLemmatizer() 
punct = [c for c in '!@#$%^&*()_+{}:"<>?-=[]\\|;\',./']
punct.append('.,')

def tokenize(sent):
    """
    When passed in a sentence, tokenizes and normalizes the string,
    returning a list of lemmata.
    """
    return "".join([lemmatizer.lemmatize(token.lower()) for token in nltk.wordpunct_tokenize(sent) if token not in punct])

## Load into memory
dirty = sorted(set(load_data('openfda-manufacturer_name.txt')))
ndirty = [(x, tokenize(x)) for x in dirty]

THRESHOLD = 0.96
matches = 0

for x in ndirty:
    #print(tokenize(x), x, sep='\t')
    for y in ndirty:
        score = distance.levenshtein(x[1], y[1])
        if score and score < 3:
          print(x[0], y[0], score, sep='\t')