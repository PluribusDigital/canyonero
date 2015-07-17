## Imports

import os
from collections import defaultdict
import csv
import nltk
import json
import math
import random
import distance 
import canyonero

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
punct = [c for c in '!@#$%^*()_+{}:"<>?-=[]\\|;\',./']
punct.append('.,')
punct.append('..')

abbrev = {
          '&': 'and',
          'labs': 'laboratory',
          'ltd': 'limited',
          'llc': 'limited',
          'inc': 'incorporated',
          'ind': 'independent',
          'co': 'company',
          'corp': 'corporation',
          'corps': 'corporation',
          'div': 'division',
          'dist': 'distributor',
          'pvt': 'private',
          'srl': 'limited',
          'lp': 'limited',
          'lc': 'limited',
          'gmbh': 'limited',
          }

def normalize(s):
    s = s.lower()
    # spell check
    # expand abbrev
    if s in abbrev:
        return abbrev[s]

    # replace nicknames
    s = lemmatizer.lemmatize(s)
    return s

def tokenize(sent):
    """
    When passed in a sentence, tokenizes and normalizes the string,
    returning a list of lemmata.
    """
    return [normalize(token) for token in nltk.wordpunct_tokenize(sent) if token not in punct]

def encode(sent):
    return "".join(tokenize(sent))

## Load into memory
dirty = load_data('openfda-manufacturer_name.txt')

## Map to grouped key-value pairs
gkv = defaultdict(list)
for v in sorted(set(dirty)):
    k = encode(v)
    gkv[k].append(v)

## Build a BK-Tree
tree = canyonero.bk_tree.BKNode('pfizer')
for k in gkv.keys():
    tree.insert(k);

with open(os.path.join(DATAPATH, 'clusters.txt'), 'w') as f:
    for k in sorted(gkv):
        relatedKeys = []
        tree.search(k, 2, relatedKeys)
        cluster = []
        for k1 in relatedKeys:
            for v in gkv[k1]:
                cluster.append(v)

        print(k, '\n'.join(cluster), 
                sep='\n', 
                end='\n=======\n', 
                file=f)
