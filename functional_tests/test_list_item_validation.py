# from django.test import LiveServerTestCase
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class LayoutAndStylingTest(FunctionalTest):

    def test_cannot_add_empty_list(self):

        # Bill se rend su rl page d'accueil et tente d'insérer une tache vide
        # accidentellement. Elle tape Enter dans la liste d'entrée.
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')


        # la page d'accueil se charge avec un message d'erreur indiquant qu'il
        # n'est pas possible de créer une nouvelle liste avec une tâche vide.
        error = self.browser.find_element_by_css_selector('.has-error') #1
        self.assertEqual(error.text, "Impossible de créer une liste avec un item qui est vide")

        # Il fait une deuxième tentative avec du texte cette-fois ci, ce qui
        # fonctionne comme prévu.
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk') #2

        # Il décide de réessayer d'envoyer un item vide et reçoit un message
        # d'erreur.
        self.get_item_input_box().send_keys('\n')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "Impossible de créer une liste avec un item qui est vide")

        # il peut corriger son erreur en remplissant le champ approprié.
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')

# ceci n'est plus utile puisque l'on utilise LiveServerTestCase et que le test
# est chargé comme un module
if __name__ == '__main__':
    unittest.main(warnings='ignore')
