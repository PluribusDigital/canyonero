import unittest
import canyonero
import json
from canyonero.nameSet import DataContext, ModelEncoder, NameCluster

ID1 = 'a09W244fRLG+RI3uHDBOtw=='

class TestNameClusterIndex(unittest.TestCase):
    def setUp(self):
        a = canyonero.App()
        self.target = a.app.test_client()
        urlFormat = '/nameset/{0}/cluster'
        self.url = a.absoluteUrl(urlFormat.format(ID1))
        self.urlBadNameSet = a.absoluteUrl(urlFormat.format('failure'))
        self.dataContext = DataContext()
        self.dataContext.beginTransaction()

    def tearDown(self):
        self.dataContext.rollBack()

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def test_get_all(self):
        rv = self.target.get(self.url + '?all')
        self.assertEqual(200, rv.status_code)

        result = json.loads(rv.data.decode('utf-8'))
        self.assertEqual(807, len(result))
        self.assertIn('link', result[0])
        self.assertIn('href', result[0]['link'])

    def test_get_ambiguous(self):
        rv = self.target.get(self.url)
        self.assertEqual(200, rv.status_code)

        result = json.loads(rv.data.decode('utf-8'))
        self.assertEqual(253, len(result))
        self.assertIn('link', result[0])
        self.assertIn('href', result[0]['link'])

    def test_get_bad_name(self):
        rv = self.target.get(self.urlBadNameSet)
        self.assertEqual(404, rv.status_code)

    def test_delete(self):
        rv = self.target.delete(self.url)
        self.assertEqual(405, rv.status_code)

    def test_put(self):
        rv = self.target.put(self.url, data={'a': '1'})
        self.assertEqual(405, rv.status_code)

    def test_post(self):
        data = json.dumps('El Em_En.Oh-Pee!')
        rv = self.target.post(self.url, data=data, 
                              content_type='application/json')

        self.assertEqual(201, rv.status_code)
        result = json.loads(rv.data.decode('utf-8'))
        self.assertIn('link', result)
        self.assertIn('href', result['link'])
        self.assertIn('elemenohpee', result['link']['href'])
        self.assertIn('key', result)

        entry = self.dataContext[result[ID1]][result['key']]
        self.assertEqual('El Em_En.Oh-Pee!', entry.canon)
        self.assertEqual(false, entry.validated)
        self.assertEqual(1, len(entry.variations))

    def test_post_duplicate(self):
        data = json.dumps('Prasco Laboratories')
        rv = self.target.post(self.url, data=data, 
                              content_type='application/json')

        self.assertEqual(409, rv.status_code)

    def test_post_bad_name(self):
        rv = self.target.post(self.urlBadNameSet, data={'a': '1'})
        self.assertEqual(404, rv.status_code)

if __name__ == '__main__':
    unittest.main()
