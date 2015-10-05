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
        self.session = '14-15'

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
