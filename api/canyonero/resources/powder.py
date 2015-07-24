## Imports

import os
import csv
import json
import pickle
from canyonero.nameSet import *

## Important Paths
INPATH = os.path.join(os.path.dirname(__file__), "../../../data/")
OUTPATH = os.path.join(os.path.dirname(__file__), "../nameSet/")

def load_data(name):
    """
    Create a generator to load data from the data source.
    """
    with open(os.path.join(INPATH, name), 'r') as f:
        reader = csv.DictReader(f, dialect='excel-tab')
        for row in reader:
            yield row['name']

## Load into memory
print('loading')
dirty = load_data('openfda-manufacturer_name.txt')

print('initializing')
nameSet = NameSet('Manufacturers', list(dirty)[:5000])
print('building')
nameSet.buildClusters()

#with open(os.path.join(DATAPATH, 'nameset_1.json'), 'w') as f:
#    json.dump(nameSet, f, cls=ModelEncoder, indent=2, sort_keys=True)
with open(os.path.join(OUTPATH, 'db.p'), 'wb') as f:
    pickle.dump([nameSet], f)