class memoize:
  def __init__(self, function):
    self.function = function
    self.memoized = {}

  def __call__(self, *args):
    try:
      return self.memoized[args]
    except KeyError:
      self.memoized[args] = self.function(*args)
      return self.memoized[args]

@memoize
def levenshtein(s1, s2):		
    ''' This implementation is from https://gist.github.com/Arachnid/491973		
    '''		
    if len(s1) < len(s2):		
        return levenshtein(s2, s1)		
    if not s1:		
        return len(s2)		

    previous_row = range(len(s2) + 1)		
    for i, c1 in enumerate(s1):		
        current_row = [i + 1]		
        for j, c2 in enumerate(s2):		
            # j+1 instead of j since previous_row and current_row are one 		
            # character longer		
            insertions = previous_row[j + 1] + 1 		
            deletions = current_row[j] + 1     # than s2		
            substitutions = previous_row[j] + (c1 != c2)		
            current_row.append(min(insertions, deletions, substitutions))		
        previous_row = current_row		

    return previous_row[-1]

class BKNode(dict):
    ''' Implementation of a Burkhard-Keller Tree
    Adapted from https://gist.github.com/Arachnid/491973
    '''
    def __init__(self, term):
        self.__dict__ = self
        self.term = term
        self.children = {}
      
    def insert(self, other):
        d = levenshtein(self.term, other)
        if d in self.children:
            self.children[d].insert(other)
        else:
            self.children[d] = BKNode(other)
  
    def search(self, term, k, results=None):
        if results is None:
            results = []
        d = levenshtein(self.term, term)
        counter = 1
        if d <= k:
            results.append(self.term)
        for i in range(max(0, d - k), d + k + 1):
            child = self.children.get(i)
            if child:
                counter += child.search(term, k, results)
        return counter