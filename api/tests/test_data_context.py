import unittest
import canyonero
from canyonero.dal import DataContext

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
            self.assertIsInstance(ns, canyonero.NameSet)
            count += 1
        self.assertEqual(1, count)

    def testGet(self):
        ns = self.target[0]
        self.assertIsInstance(ns, canyonero.NameSet)

    def testUpdate(self):
        ns = self.target[0]
        self.assertIsInstance(ns, canyonero.NameSet)
        ns.title = 'A new title'
        self.target[0] = ns
        
        ctxt = DataContext()
        self.assertEqual('A new title', ctxt[0].title)

    def testDelete(self):
        del self.target[0]
        self.assertIsNone(self.target[0])
        self.assertEqual(0, len(self.target))

if __name__ == '__main__':
    unittest.main()
