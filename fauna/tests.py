from typing import Dict

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
from fauna.choices import PERIOD_CHOICES
from fauna.models import Animal


class AnimalTestCase(APITestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_get_empty_list_of_animals_on_endpoint(self):
        res = self.client.get(reverse("animals-list"))
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(len(res.data["results"]), 0)

    def test_get_existing_animal_on_endpoint(self):
        animal_params = dict(period=PERIOD_CHOICES[6][0],
                             extinction="Our very own",
                             name="carrier pigeon",
                             taxonomy_class="Aves",
                             taxonomy_order="Columbiformes",
                             taxonomy_family="Columbidae")
        self.given_animal_exists(animal_params)

        res = self.client.get(reverse("animals-list"))
        self.assertEqual(len(res.data["results"]), 1)

        first_result = res.data["results"][0]

        self.assertEqual(first_result["name"], "carrier pigeon")

    def given_animal_exists(self, animal_params:Dict[str, str]):
        Animal.objects.create(**animal_params)