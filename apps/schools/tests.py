"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from rest_framework.test import APITestCase, APIClient
from schools.api_views import api_root
from django.core.urlresolvers import reverse


class EndpointTest(APITestCase):
    def setUp(self):
        # Using the standard RequestFactory API to create a form POST request
        self.client = APIClient()
        self.session = '16-17'
        self.valid_dise_code = 29230801501

    def test_root(self):
        """
        Just for testing that things are OK
        """
        response = self.client.get(reverse('api_root'))
        self.assertEqual(response.status_code, 200)
        # no key named 'error'
        self.assertNotIn('error', response.data.keys())

    def test_search(self):
        """
        Search all the things
        """
        response = self.client.get(
            reverse('api_search', args=(self.session,)) + '?type=all&query=pura'
        )
        # result is a list of entity types
        self.assertIsInstance(response.data, list)
        # there are 5 types of entities right now
        self.assertEqual(len(response.data), 5)

    def test_school_list(self):
        """
        List of schools
        """
        response = self.client.get(
            reverse('api_school_list', args=(self.session,)) + '?management=govt&area=urban'
        )
        # no error
        self.assertNotIn('error', response.data.keys())
        # there are more than 0 results
        self.assertNotEqual(response.data.get('count'), 0)

    def test_invalid_school(self):
        """
        Invalid DISE code - 2923080151
        """
        response = self.client.get(
            reverse('api_school_info', args=(self.session, 123456))
        )
        # got error
        self.assertEqual(response.data.get('detail'), "Not found.")

    def test_valid_school(self):
        """
        Valid DISE code - 29230801501
        """
        response = self.client.get(
            reverse('api_school_info', args=(self.session, self.valid_dise_code))
        )
        # got error
        self.assertEqual(response.data.get('id'), self.valid_dise_code)

    def test_aggregate_list(self):
        response = self.client.get(reverse('api_entity_list', args=(self.session, 'district')))
        self.assertNotEqual(response.data.get('count'), 0)

    def test_aggregate_info(self):
        response = self.client.get(reverse('api_entity_info', args=(self.session, 'district', 'bagalkot')))
        self.assertNotEqual(response.data.get('properties').get('sum_has_toilet'), 0)

    def test_aggregate_school_list(self):
        response = self.client.get(reverse('api_entity_school_list', args=(self.session, 'district', 'bagalkot')))
        self.assertNotEqual(response.data.get('count'), 0)

    def test_clusters_in_block(self):
        response = self.client.get(reverse('api_clusters_in_block', args=(self.session, 'block', 'bagalkot-badami')))
        self.assertNotEqual(response.data.get('count'), 0)

    def test_clusters_in_district(self):
        response = self.client.get(reverse('api_clusters_in_district', args=(self.session, 'district', 'bagalkot')))
        self.assertNotEqual(response.data.get('count'), 0)

    def test_blocks_in_district(self):
        response = self.client.get(reverse('api_blocks_in_district', args=(self.session, 'district', 'bagalkot')))
        self.assertNotEqual(response.data.get('count'), 0)
