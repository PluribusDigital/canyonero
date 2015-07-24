import unittest
import canyonero

class Test_RootEndpoint(unittest.TestCase):
    def setUp(self):
        flaskInstance = canyonero.App()
        self.target = flaskInstance.app.test_client()

    def test_get(self):
        rv = self.target.get('/')
        print(rv)
        assert b'Link' in rv.data

if __name__ == '__main__':
    unittest.main()
