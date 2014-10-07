from django.test import TestCase

# test pour tester que les tests fonctionnent
class SmokeTest(TestCase):
    def test_bad_maths(self):
        self.assertEqual(1 + 1, 3)