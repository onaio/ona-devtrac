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
