# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

import sys


class FunctionalTest(StaticLiveServerTestCase):

    # TODO: lorsqu'on utilise un 'staging site', il faut adapter ces tests
    # pour pouvoir les exécuter sur ce serveur, notamment, il faudra utiliser
    # desméthodes de classe pour setUp et tearDown. Cf http://chimera.labs.oreilly.com/books/1234000000754/ch08.html#_as_always_start_with_a_test

    @classmethod
    def setUpClass(cls):  #1
        for arg in sys.argv:  #2
            if 'liveserver' in arg:  #3
                cls.server_url = 'http://' + arg.split('=')[1]  #4
                return  #5
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        # demande à Selenium d'attendre 3 secondes si nécessaire (chargement
        # de la page) avant de faire les tests
        self.browser.implicitly_wait(1)

    def tearDown(self):
        # pour éviter les erreurs stupides dans Windows
        self.browser.refresh()
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

# ceci n'est plus utile puisque l'on utilise LiveServerTestCase et que le test
# est chargé comme un module
if __name__ == '__main__':
    unittest.main(warnings='ignore')
