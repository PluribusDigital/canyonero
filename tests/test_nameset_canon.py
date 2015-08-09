import unittest
import canyonero
import json

class TestNameSetCanon(unittest.TestCase):
    def setUp(self):
        a = canyonero.App()
        self.target = a.app.test_client()
        urlFormat = '/nameset/{0}/canon'
        self.url = a.absoluteUrl(urlFormat.format('XTfIPZmASrK89OeK9phOhQ'))
        self.urlBadNameSet = a.absoluteUrl(urlFormat.format('failure'))

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def test_get(self):
        rv = self.target.get(self.url)
        self.assertEqual(200, rv.status_code)

        canon = json.loads(rv.data.decode('utf-8'))
        self.assertEqual(1254, len(canon))

    def test_get_bad(self):
        rv = self.target.get(self.urlBadNameSet)
        self.assertEqual(404, rv.status_code)

    def test_delete(self):
        rv = self.target.delete(self.url)
        self.assertEqual(405, rv.status_code)

    def test_post(self):
        rv = self.target.post(self.url, data={'a': '1'})
        self.assertEqual(405, rv.status_code)

    def test_put(self):
        rv = self.target.get(self.url)
        rv = self.target.put(self.url, data=rv.data, 
                              content_type='application/json')
        self.assertEqual(405, rv.status_code)

if __name__ == '__main__':
    unittest.main()
