import unittest
import canyonero
import json

class Test_RootEndpoint(unittest.TestCase):
    def setUp(self):
        flaskInstance = canyonero.App()
        self.target = flaskInstance.app.test_client()

    def test_get(self):
        rv = self.target.get('/')
        self.assertEqual(200, rv.status_code)

        result = json.loads(rv.data.decode('utf-8'))
        self.assertEqual(1, len(result))
        self.assertIn('link', result[0])
        self.assertIn('href', result[0]['link'])
        self.assertIn('nameset', result[0]['link']['href'])

if __name__ == '__main__':
    unittest.main()
