"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import RequestFactory
from django.test.client import Client
import json


class EndpointTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.client = Client()

    def test_endpoints(self):
        """
        Just for testing that things are OK
        """
        response = self.client.get('/api/drf/')
        self.assertEqual(response.status_code, 200)

        print 'Testing that all the endpoints are alive'
        for endpoint in response.data.values():
            print endpoint
            eresp = self.client.get(endpoint)
            self.assertEqual(
                eresp.status_code, 200,
                'Found %s during %s' % (eresp.status_code, endpoint)
            )
