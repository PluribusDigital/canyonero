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
                'threshold' : obj.threshold,
                'clusters': obj.clusters
                } 
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

    @classmethod
    def decodeNameSet(cls, s):
        o = json.loads(s)
        if 'names' not in o:
            return None

        title = o['title'] if 'abbrev' in o else self.defaultTitle()
        ns = NameSet(title, o['names'])
        if 'abbrev' in o:
            ns.abbrev = o['abbrev']
        if 'ignore' in o:
            ns.ignore = o['ignore']
        if 'clusters' in o:
            ns.clusters = o['clusters']
        if 'threshold' in o:
            ns.threshold = o['threshold']
        return ns

    @classmethod
    def decodeCluster(cls, s):
        return None
