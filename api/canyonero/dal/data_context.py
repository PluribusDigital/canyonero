import os
import json
import pickle
from canyonero.models import NameSet
from canyonero.dal import ModelEncoder

#------------------------------------------------------------------------------
# The "Database"
#------------------------------------------------------------------------------

DATAPATH = os.path.dirname(__file__)

_cache = []

def cache():
    global _cache
    if not _cache:
        with open(os.path.join(DATAPATH, 'db.p'), 'rb') as f:
            _cache = pickle.load(f)
    return _cache

#------------------------------------------------------------------------------
# Access the database
#------------------------------------------------------------------------------

class DataContext():
    """ Represents the database interface, even though not implemented
    """
    def __init__(self):
        pass

    def __contains__(self, item):
        return item in cache()

    def __len__(self):
        n = 0
        for nameSet in cache():
            if nameSet:
                n += 1
        return n

    def __iter__(self):
        for nameSet in cache():
            if nameSet:
                yield nameSet

    def __getitem__(self, key):
        return cache()[key]

    def __setitem__(self, key, value):
        cache()[key] = value
        # then save

    def __delitem__(self, key):
        cache()[key] = None
        # then save

if __name__ == '__main__':
    ctxt = DataContext()
    print(json.dumps(ctxt[0], cls=ModelEncoder))
    print(len(ctxt))
    del ctxt[0]
    print(json.dumps(ctxt[0], cls=ModelEncoder))
    print(len(ctxt))
