import unittest
import canyonero
import json
from canyonero.nameSet import DataContext, NameSet, ModelEncoder

class TestNameSetDetail(unittest.TestCase):
    def setUp(self):
        a = canyonero.App()
        self.target = a.app.test_client()
        self.baseUrl = a.absoluteUrl('/nameset/')
        self.url = self.baseUrl + 'XTfIPZmASrK89OeK9phOhQ'
        self.urlBadNameSet = self.baseUrl + 'fail'
        self.dataContext = DataContext()
        self.dataContext.beginTransaction()

    def tearDown(self):
        self.dataContext.rollBack()

    # -------------------------------------------------------------------------
    # Test Helpers
    # -------------------------------------------------------------------------

    def toNameSet(self, rv):
        return ModelEncoder.decode(rv.data.decode('utf-8'))

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def test_get(self):
        rv = self.target.get(self.url)
        self.assertEqual(200, rv.status_code)

        ns = self.toNameSet(rv)
        self.assertEqual('Manufacturers', ns.title)
        self.assertEqual(1254, len(ns.names))
        self.assertEqual(807, len(ns.clusters))
        self.assertEqual(31, len(ns.ignore))
        self.assertEqual(4, len(ns.abbrev))

    def test_get_bad(self):
        rv = self.target.get(self.urlBadNameSet)
        self.assertEqual(404, rv.status_code)

    def test_get_recalculate(self):
        rv = self.target.get(self.url + '?recalculate=0')
        self.assertEqual(200, rv.status_code)

        ns = self.toNameSet(rv)
        self.assertEqual('Manufacturers', ns.title)
        self.assertEqual(1254, len(ns.names))
        self.assertEqual(873, len(ns.clusters))
        self.assertEqual(31, len(ns.ignore))
        self.assertEqual(4, len(ns.abbrev))

    def test_delete(self):
        rv = self.target.delete(self.url)
        self.assertEqual(204, rv.status_code)
        self.assertEqual(0, len(self.dataContext))

    def test_delete_bad(self):
        rv = self.target.delete(self.urlBadNameSet)
        self.assertEqual(404, rv.status_code)
        self.assertEqual(1, len(self.dataContext))

    def test_post(self):
        rv = self.target.post(self.url, data={'a': '1'})
        self.assertEqual(405, rv.status_code)

    def test_put(self):
        rv = self.target.get(self.url)
        rv = self.target.put(self.url, data=rv.data, 
                              content_type='application/json')

        self.assertEqual(200, rv.status_code)

    def test_put_bad_format(self):
        rv = self.target.put(self.url, data={'a': '1'})
        self.assertEqual(400, rv.status_code)

    def test_put_bad(self):
        rv = self.target.put(self.urlBadNameSet, data={'a': '1'})
        self.assertEqual(404, rv.status_code)

if __name__ == '__main__':
    unittest.main()
