import unittest
import canyonero
import json
from canyonero.nameSet import DataContext, NameSet, ModelEncoder

ID1 = 'a09W244fRLG+RI3uHDBOtw=='

class TestNameSetIndex(unittest.TestCase):
    def setUp(self):
        a = canyonero.App()
        self.target = a.app.test_client()
        self.url = a.absoluteUrl('/nameset')
        self.dataContext = DataContext()
        self.dataContext.beginTransaction()

    def tearDown(self):
        self.dataContext.rollBack()

    def names(self):
        return ['Echo & The Bunnymen',
                'Echo & The Bunnyman',
                'Echo and the Bunnymen',
                'Echo + the Bunnymen',
                'Kool and the Gang'
               ]

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def test_get(self):
        rv = self.target.get(self.url)
        self.assertEqual(200, rv.status_code)

        result = json.loads(rv.data.decode('utf-8'))
        self.assertEqual(1, len(result))
        self.assertIn('link', result[0])
        self.assertIn('href', result[0]['link'])
        self.assertIn(ID1, result[0]['link']['href'])

    def test_delete(self):
        rv = self.target.delete(self.url)
        self.assertEqual(405, rv.status_code)

    def test_put(self):
        rv = self.target.put(self.url, data={'a': '1'})
        self.assertEqual(405, rv.status_code)

    def test_post_list(self):
        data = json.dumps(self.names())
        rv = self.target.post(self.url, data=data, 
                              content_type='application/json')

        self.assertEqual(201, rv.status_code)
        result = json.loads(rv.data.decode('utf-8'))
        self.assertIn('link', result)
        self.assertIn('href', result['link'])
        self.assertIn('id', result)

        entry = self.dataContext[result['id']]
        self.assertEqual(2, len(entry.clusters))

    def test_post_name_set(self):
        ns = NameSet('Bands', self.names())
        data = json.dumps(ns, cls=ModelEncoder)

        rv = self.target.post(self.url, data=data, 
                              content_type='application/json')

        self.assertEqual(201, rv.status_code)
        result = json.loads(rv.data.decode('utf-8'))
        self.assertIn('link', result)
        self.assertIn('href', result['link'])
        self.assertIn('id', result)

        entry = self.dataContext[result['id']]
        self.assertEqual(2, len(entry.clusters))

    def test_post_bad(self):
        rv = self.target.post(self.url, data={'a': '1'})
        self.assertEqual(400, rv.status_code)

if __name__ == '__main__':
    unittest.main()
