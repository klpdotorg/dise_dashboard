"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import RequestFactory
from django.test.client import Client


class EndpointTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.client = Client()

    def test_school_endpoints(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        response = self.client.get('/api/v1/olap/', {
            'method': 'School.search',
            'session': '10-11',
            'name': 'govt',
            'bbox': '75.73974609375,12.5223906020692,79.4476318359375,13.424352095715332'
        })
        self.assertEqual(response.status_code, 200)
