import unittest
import canyonero
import json
from canyonero.nameSet import DataContext

ID1 = 'a09W244fRLG+RI3uHDBOtw=='

class TestNameSetAbbrev(unittest.TestCase):
    def setUp(self):
        a = canyonero.App()
        self.target = a.app.test_client()
        urlFormat = '/nameset/{0}/abbrev'
        self.url = a.absoluteUrl(urlFormat.format(ID1))
        self.urlBadNameSet = a.absoluteUrl(urlFormat.format('failure'))
        self.dataContext = DataContext()
        self.dataContext.beginTransaction()

    def tearDown(self):
        self.dataContext.rollBack()


    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def test_get(self):
        rv = self.target.get(self.url)
        self.assertEqual(200, rv.status_code)

        abbrev = json.loads(rv.data.decode('utf-8'))
        self.assertEqual(4, len(abbrev))

    def test_get_bad(self):
        rv = self.target.get(self.urlBadNameSet)
        self.assertEqual(404, rv.status_code)

    def test_put_with_calc(self):
        rv = self.target.get(self.url)
        rv = self.target.put(self.url + '?recalculate=0', data=rv.data, 
                              content_type='application/json')
        self.assertEqual(204, rv.status_code)

        ns = self.dataContext[ID1]
        self.assertEqual(873, len(ns.clusters))

    def test_put_without_calc(self):
        rv = self.target.put(self.url, data=json.dumps({'+' : 'and'}), 
                              content_type='application/json')
        self.assertEqual(205, rv.status_code)

        ns = self.dataContext[ID1]
        self.assertEqual(807, len(ns.clusters))

    def test_put_bad_nameset(self):
        rv = self.target.put(self.urlBadNameSet, data={'a': '1'})
        self.assertEqual(404, rv.status_code)

    def test_put_bad_format(self):
        rv = self.target.put(self.url, data=json.dumps(['a', '1']))
        self.assertEqual(400, rv.status_code)

    def test_delete_without_calc(self):
        rv = self.target.delete(self.url)
        self.assertEqual(205, rv.status_code)

        ns = self.dataContext[ID1]
        self.assertEqual(807, len(ns.clusters))

    def test_delete_with_calc(self):
        rv = self.target.delete(self.url + '?recalculate=0')
        self.assertEqual(204, rv.status_code)

        ns = self.dataContext[ID1]
        self.assertEqual(881, len(ns.clusters))

    def test_delete_bad(self):
        rv = self.target.delete(self.urlBadNameSet)
        self.assertEqual(404, rv.status_code)

    def test_post(self):
        rv = self.target.post(self.url, data={'a': '1'})
        self.assertEqual(405, rv.status_code)

if __name__ == '__main__':
    unittest.main()
