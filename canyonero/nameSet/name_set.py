import unicodedata
import sys
import nltk
import uuid
import binascii
from collections import defaultdict
from canyonero.analysis import *
from canyonero.nameSet import *

def generateID():
    """Generates and ID that will be unique and safe to include in a URL"""
    id = uuid.uuid4()
    bytes = binascii.b2a_base64(id.bytes)
    s = bytes.decode('utf-8').strip()
    s = s.strip('=')
    s = s.replace('+', '-')
    s = s.replace('/', '_')
    return s

class NameSet():
    """ The organizing structure for determining the canonical \
    representation from a set of strings
    """
    def __init__(self, title, names=[]):
        ''' `title` is the name of this set of data. (Artists, Manufacturers)
        `names` is an array of strings that need to be processed
        '''
        self.abbrev = self._defaultAbbrev()
        self.ignore = self._defaultIgnore()
        self.charTranslate = self._defaultCharTranslate()
        self.charExpansion = self._defaultCharExpansion()

        self.names = names
        self.title = title
        self.threshold = 2

        self.id = generateID()

    # -------------------------------------------------------------------------
    # ID
    # -------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    # Default normalizing lists
    #--------------------------------------------------------------------------

    @classmethod
    def _defaultAbbrev(cls):
        """ Creates the default set of abbreviations.
        Abbreviations replace a string with another string
        """
        return {
            'ltd': 'limited',
            'llc': 'limited',
            'inc': 'incorporated',
            'corp': 'corporation'
            }

    @classmethod
    def _defaultIgnore(cls):
        """ Creates the default list of tokens to ignore
        """
        ignore = [c for c in '!@#$%^*()_{}:"<>?-=[]\\|;\',./']
        ignore.append('the')
        ignore.append('a')
        ignore.append('an')
        return ignore

    @classmethod
    def _defaultCharExpansion(cls):
        ''' Creates the default table used to replace single characters with \
        a string
        '''
        table = {}
        table['&'] = 'and'
        table['+'] = 'and'
        table['\xdf'] = 'ss'  # sharp s
        table['\xe6'] = 'ae'  # ligature
        table['\xfe'] = 'th'  # thorn
        return table

    @classmethod
    def _defaultCharTranslate(cls):
        ''' Creates the default table for replacing accented and non-english \
        characters with an ASCII equivalent.  
        This only works for single character replacement.
        '''
        table = {}
        if sys.version >= '3':
            table = dict.fromkeys(c for c in range(sys.maxunicode)
                                  if unicodedata.combining(chr(c)))
        else:
            table = dict.fromkeys(c for c in range(sys.maxunicode)
                                  if unicodedata.combining(unichr(c)))

        # latin extended not handled by decombining
        table[0xf0] = ord('d')   # eth

        # greek
        table[0x3b1] = ord('a')
        table[0x3b4] = ord('d')

        return table

    #--------------------------------------------------------------------------
    # Normalizing Functions
    #--------------------------------------------------------------------------

    def _expandCharacters(self, s):
        s0 = s
        for c in s:
            if c in self.charExpansion:
                s0 = s0.replace(c, self.charExpansion[c])
        return s0

    def _normalize(self, s):
        # remove non-ASCII
        b = unicodedata.normalize('NFKD', s.lower())
        s = b.translate(self.charTranslate)

        # it is in the ignore list
        if s in self.ignore:
            return ''

        # spell check

        # expand characters
        s = self._expandCharacters(s)

        # expand abbreviations
        if s in self.abbrev:
            s = self.abbrev[s]

        # replace nicknames

        # lemmatize (foxes => fox)
        s = self.lemmatizer.lemmatize(s)
        return s

    def _tokenize(self, words):
        """
        Returns a list of normalized, tokenized, lemmata.
        """
        return [self._normalize(token) 
                for token in nltk.wordpunct_tokenize(words)]

    def makeClusterKey(self, words):
        """ Creates the key from a set of words
        """
        return "".join(self._tokenize(words))

    #--------------------------------------------------------------------------
    # Properties
    #--------------------------------------------------------------------------

    @property
    def names(self):
        return self._names

    @names.setter
    def names(self, value):
        self._names = list(set(value))
        self.clusters = {}

    @property
    def threshold(self):
        return getattr(self, '_threshold', 2)

    @threshold.setter
    def threshold(self, value):
        self._threshold = value

    #--------------------------------------------------------------------------
    # Main Methods
    #--------------------------------------------------------------------------

    def buildClusters(self):
        ''' Creates clusters from the set of names
        '''
        # reset
        self.clusters = {}

        # no names, no work
        if len(self._names) == 0:
            return

        self.lemmatizer = nltk.WordNetLemmatizer() 
        
        # Map to grouped key-value pairs
        print("  Creating grouped key-value pairs", end=' ')
        gkv = defaultdict(list)
        for v in sorted(self._names):
            k = self.makeClusterKey(v)
            gkv[k].append(v)
        print(len(gkv))

        # Build a BK-Tree
        print("  Building B-K Tree")
        tree = BKNode(self._names[0])
        for k in gkv.keys():
            tree.insert(k);

        # get the list of keys - the gkv will change during iteration
        keys = sorted(gkv)

        # Build the clusters
        print("  Build the clusters from the B-K Tree", end=' ')
        for k in keys:
            relatedKeys = []
            tree.search(k, self.threshold, relatedKeys)
            
            cluster = NameCluster(k)
            for k1 in relatedKeys:
                if k1 in gkv:
                    for v in gkv[k1]:
                        cluster.variations.append(v)
                    del gkv[k1]

            cluster.onComplete()
            if cluster.variations:
                self.clusters[k] = cluster
        print(len(self.clusters))
