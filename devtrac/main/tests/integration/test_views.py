from django.core.urlresolvers import reverse
from django.test import Client, TestCase


class HomeViewTest(TestCase):
    def test_home_view(self):
        home_url = reverse('home')
        client = Client()
        response = client.get(home_url)
        self.assertContains(response, 'Devtrac Bridge')
