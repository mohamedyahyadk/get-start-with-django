from django.test import TestCase
from django.shortcuts import reverse
# Create your tests here.
class LandingPageTest(TestCase):
    def test_get(self):
        #Todo some sort of test
        response=self.client.get(reverse("landing_page"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"landing.html")
        pass
