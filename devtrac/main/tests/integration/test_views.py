from django.core.urlresolvers import reverse
from django.test import Client

from devtrac.main.tests.test_base import TestBase


class HomeViewTest(TestBase):
    def test_home_view(self):
        self._add_submission()
        home_url = reverse('home')
        client = Client()
        response = client.get(home_url)
        self.assertContains(response, 'Total number of reports: 1')


class FieldTripTest(TestBase):
    def test_fieldtrips_csv_view(self):
        self._add_submission()
        url = reverse('fieldtrips', kwargs={'format': 'csv'})
        client = Client()
        response = client.get(url)

        self.assertContains(response, 'fieldtrip_key,nid,title')
