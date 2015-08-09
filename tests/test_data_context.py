import unittest
from canyonero.nameSet import *

ID = 'XTfIPZmASrK89OeK9phOhQ'

class TestDataContext(unittest.TestCase):
    def setUp(self):
        self.target = DataContext()
        self.target.beginTransaction()

    def tearDown(self):
        self.target.rollBack()

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def testCount(self):
        self.assertEqual(1, len(self.target))

    def testGetAll(self):
        count = 0
        for ns in self.target:
            self.assertIsInstance(ns, NameSet)
            count += 1
        self.assertEqual(1, count)

    def testGet(self):
        ns = self.target[ID]
        self.assertIsInstance(ns, NameSet)

    def testUpdate(self):
        ns = self.target[ID]
        self.assertIsInstance(ns, NameSet)
        ns.title = 'A new title'
        self.target[ID] = ns
        
        ctxt = DataContext()
        self.assertEqual('A new title', ctxt[ID].title)

    def testSet(self):
        ns = NameSet('Testing', ['a', 'b', 'c'])
        self.target[ns.id] = ns
        self.assertEqual(2, len(self.target))

    def testDelete(self):
        del self.target[ID]
        self.assertEqual(0, len(self.target))

if __name__ == '__main__':
    unittest.main()
