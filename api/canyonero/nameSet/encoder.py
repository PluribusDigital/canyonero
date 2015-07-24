import json
from canyonero.nameSet import *

class ModelEncoder(json.JSONEncoder):
     def default(self, obj):
         if isinstance(obj, NameCluster):
             return { 
                 'canon': obj.canon,
                 'key' : obj.key,
                 'validated': obj.validated,
                 'variations': sorted(obj.variations)
                 } 
         elif isinstance(obj, NameSet):
             return {
                 'abbrev': obj.abbrev,
                 'ignore' : sorted(obj.ignore),
                 'names': sorted(obj.names),
                 'title': obj.title,
                 'clusters': obj.clusters
                 } 
         # Let the base class default method raise the TypeError
         return json.JSONEncoder.default(self, obj)
