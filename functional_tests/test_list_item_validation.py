# from django.test import LiveServerTestCase
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class LayoutAndStylingTest(FunctionalTest):

    @skip
    def test_cannot_add_empty_list(self):

        # Bill se rend su rl page d'accueil et tente d'insérer une tache vide
        # accidentellement. Elle tape Enter dans la liste d'entrée.

        # la page d'accueil se charge avec un message d'erreur indiquant qu'il
        # n'est pas possible de créer une nouvelle liste avec une tâche vide.

        # Il fait une deuxième tentative avec du texte cette-fois ci, ce qui
        # fonctionne comme prévu.

        # Il décide de réessayer d'envoyer un item vide et reçoit un message
        # d'erreur.

        # il peut corriger son erreur en remplissant le champ approprié.
        self.fail("Write Me !!!")

# ceci n'est plus utile puisque l'on utilise LiveServerTestCase et que le test
# est chargé comme un module
if __name__ == '__main__':
    unittest.main(warnings='ignore')
