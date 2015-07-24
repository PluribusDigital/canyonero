
class NameCluster():
    """Holds one cluster of names"""
    def __init__(self, key):
        self.canon = ''
        self.key = key
        self.validated = False
        self.variations = []

    def onComplete(self):
        """This is called when the cluster has finished building"""
        count = len(self.variations)
        self.validated = (count == 1)
        self.canon = ''
        for i in range(0, count):
            if len(self.variations[i]) > len(self.canon):
                self.canon = self.variations[i]


