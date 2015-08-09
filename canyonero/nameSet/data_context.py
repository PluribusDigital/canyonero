import os
import json
import pickle

#------------------------------------------------------------------------------
# The "Database"
#------------------------------------------------------------------------------

DATAPATH = os.path.dirname(__file__)

_cache = None

def cache():
    global _cache
    if _cache == None:
        reset()
    return _cache

def reset():
    global _cache
    with open(os.path.join(DATAPATH, 'db.p'), 'rb') as f:
        _cache = pickle.load(f)

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
        return len(cache())

    def __iter__(self):
        c = cache() # verify it is loaded
        for k in c:
            yield c[k]

    def __getitem__(self, key):
        return cache()[key]

    def __setitem__(self, key, value):
        cache()[key] = value
        # then save

    def __delitem__(self, key):
        del cache()[key]
        # then save

    # -------------------------------------------------------------------------
    # Transaction functions
    # -------------------------------------------------------------------------
    def beginTransaction(self):
        pass

    def commit(self):
        pass
    
    def rollBack(self):
        reset()
