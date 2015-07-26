## Imports

import os
import csv
import json
import pickle
from canyonero.nameSet import *

## Important Paths
INPATH = os.path.join(os.path.dirname(__file__), "../../../data/")
OUTPATH = os.path.join(os.path.dirname(__file__), "../nameSet/")

#def load_data(name):
#    """
#    Create a generator to load data from the data source.
#    """
#    with open(os.path.join(INPATH, name), 'r') as f:
#        reader = csv.DictReader(f, dialect='excel-tab')
#        for row in reader:
#            yield row['name']

### Load into memory
#print('loading')
#dirty = load_data('openfda-manufacturer_name.txt')

#print('initializing')
#nameSet = NameSet('Manufacturers', list(dirty))
#print('building')
#nameSet.buildClusters()

with open(os.path.join(OUTPATH, 'db.p'), 'rb') as f:
    db = pickle.load(f)

for k in db:
    db[k].id = name_set.generateID()

with open(os.path.join(OUTPATH, 'db.p'), 'wb') as f:
    pickle.dump({x.id: x for x in db.values()}, f)