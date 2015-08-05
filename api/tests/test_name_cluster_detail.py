import unittest
import canyonero
import json
from canyonero.nameSet import DataContext, ModelEncoder, NameCluster

ID1 = 'XTfIPZmASrK89OeK9phOhQ'
CLUSTER1 = 'actavispharmaincorporated'
CLUSTER2 = 'aptalispharmaincorporated'

class TestNameClusterDetail(unittest.TestCase):
    def setUp(self):
        a = canyonero.App()
        self.target = a.app.test_client()
        urlFormat = a.absoluteUrl('/nameset/{0}/cluster/{1}')
        self.url = urlFormat.format(ID1, CLUSTER1)
        self.urlBadNameSet = urlFormat.format('failure', CLUSTER1)
        self.urlBadCluster = urlFormat.format(ID1, 'failure')

        self.queryTransfer = '?variantToTransfer={0}&transferToCluster={1}'
        self.queryNewCluster = '?newClusterFromVariant={0}'
        self.queryAsCanon = '?setAsCanon={0}'

        self.dataContext = DataContext()
        self.dataContext.beginTransaction()

    def tearDown(self):
        self.dataContext.rollBack()

    # -------------------------------------------------------------------------
    # Test Helpers
    # -------------------------------------------------------------------------

    def toCluster(self, rv):
        return ModelEncoder.decodeCluster(rv.data.decode('utf-8'))

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def test_get(self):
        rv = self.target.get(self.url)
        self.assertEqual(200, rv.status_code)

        result = self.toCluster(rv)
        self.assertEqual('Actavis Pharma, Inc.', result.canon)
        self.assertEqual(CLUSTER1, result.key)
        self.assertEqual(False, result.validated)
        self.assertEqual(3, len(result.variations))

    def test_get_bad_name(self):
        rv = self.target.get(self.urlBadNameSet)
        self.assertEqual(404, rv.status_code)

    def test_get_bad_cluster(self):
        rv = self.target.get(self.urlBadCluster)
        self.assertEqual(404, rv.status_code)

    def test_delete(self):
        rv = self.target.delete(self.url)
        self.assertEqual(405, rv.status_code)

    def test_put(self):
        rv = self.target.put(self.url, data={'a': '1'})
        self.assertEqual(405, rv.status_code)

    def test_post_no_arg(self):
        rv = self.target.post(self.url, data={'a': '1'})
        self.assertEqual(400, rv.status_code)

    def test_post_transfer_missing_cluster(self):
        query = '?variantToTransfer={0}'.format(2)
        rv = self.target.post(self.url + query)
        self.assertEqual(400, rv.status_code)

    def test_post_transfer_missing_variant(self):
        query = '?transferToCluster={0}'.format(CLUSTER2)
        rv = self.target.post(self.url + query)
        self.assertEqual(400, rv.status_code)

    def test_post_transfer_variant_str(self):
        query = self.queryTransfer.format('Aptalis Pharma Inc.', CLUSTER2)
        rv = self.target.post(self.url + query)
        self.assertEqual(205, rv.status_code)

    def test_post_transfer_variant_int(self):
        query = self.queryTransfer.format(2, CLUSTER2)
        rv = self.target.post(self.url + query)
        self.assertEqual(205, rv.status_code)

    def test_post_transfer_bad_cluster(self):
        query = self.queryTransfer.format(2, 'notthere')
        rv = self.target.post(self.url + query)
        self.assertEqual(400, rv.status_code)

    def test_post_transfer_bad_variant_str(self):
        query = self.queryTransfer.format('Aptalis Pharma', CLUSTER2)
        rv = self.target.post(self.url + query)
        self.assertEqual(400, rv.status_code)

    def test_post_transfer_bad_variant_int(self):
        query = self.queryTransfer.format(7, CLUSTER2)
        rv = self.target.post(self.url + query)
        self.assertEqual(400, rv.status_code)

    def test_post_new_cluster_variant_str(self):
        ns = self.dataContext[ID1]
        del ns.clusters[CLUSTER2]

        query = self.queryNewCluster.format('Aptalis Pharma Inc.')
        rv = self.target.post(self.url + query)
        self.assertEqual(205, rv.status_code)

    def test_post_new_cluster_variant_int(self):
        ns = self.dataContext[ID1]
        del ns.clusters[CLUSTER2]

        query = self.queryNewCluster.format(2)
        rv = self.target.post(self.url + query)
        self.assertEqual(205, rv.status_code)

    def test_post_new_cluster_bad_variant_str(self):
        query = self.queryNewCluster.format('Aptalis Pharma')
        rv = self.target.post(self.url + query)
        self.assertEqual(400, rv.status_code)

    def test_post_new_cluster_bad_variant_int(self):
        query = self.queryNewCluster.format(7)
        rv = self.target.post(self.url + query)
        self.assertEqual(400, rv.status_code)

    def test_post_new_cluster_conflict(self):
        query = self.queryNewCluster.format(0)
        rv = self.target.post(self.url + query)
        self.assertEqual(409, rv.status_code)

    def test_post_set_as_canon_variant_str(self):
        query = self.queryAsCanon.format('Aptalis Pharma Inc.')
        rv = self.target.post(self.url + query)
        self.assertEqual(204, rv.status_code)

    def test_post_set_as_canon_variant_int(self):
        query = self.queryAsCanon.format(2)
        rv = self.target.post(self.url + query)
        self.assertEqual(204, rv.status_code)

    def test_post_set_as_canon_bad_variant_str(self):
        query = self.queryAsCanon.format('Aptalis Pharma')
        rv = self.target.post(self.url + query)
        self.assertEqual(400, rv.status_code)

    def test_post_set_as_canon_bad_variant_int(self):
        query = self.queryAsCanon.format(7)
        rv = self.target.post(self.url + query)
        self.assertEqual(400, rv.status_code)

    def test_post_too_many_cooks(self):
        q2 = self.queryAsCanon.replace('?', '&')
        q3 = self.queryNewCluster.replace('?', '&')
        q1 = self.queryTransfer + q2 + q3
        query = q1.format('Aptalis Pharma Inc.', CLUSTER2)
        rv = self.target.post(self.url + query)
        self.assertEqual(400, rv.status_code)

    def test_post_bad_nameset(self):
        rv = self.target.post(self.urlBadNameSet)
        self.assertEqual(404, rv.status_code)

    def test_post_bad_cluster(self):
        rv = self.target.post(self.urlBadCluster)
        self.assertEqual(404, rv.status_code)

if __name__ == '__main__':
    unittest.main()
