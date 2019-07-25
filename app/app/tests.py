from django.test import TestCase
from app.calc import add, subtract

class calsTest(TestCase):
    def test_add_number(self):
        self.assertEqual(add(3,8),11)
    def test_subtract_number(self):
        self.assertEqual(subtract(5,11),6)