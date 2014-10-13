from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # demande à Selenium d'attendre 3 secondes si nécessaire (chargement
        # de la page) avant de faire les tests
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Bill a entendu parler d'un nouveau site permettant de gérer ses
        # tâches. Il se dépeche de visiter le site de développement
        self.browser.get('https://tdd-c9-donnerc.c9.io/')

        # il remarque que la page a un titre et un en-têtequi contient le mot
        # 'To-Do'
        # wait = input('press any key to continue ...')
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # il voit qu'il y a un champ d'entrée de type texte dans lequel il
        # peut taper sa tâche
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Saisir votre tâche ici'
        )

        # il entre la première chose à faire le matin
        inputbox.send_keys('Rendre grâce au Créateur')

        # lorsqu'elle presse sur la touche ENTER, la page se raffraichit et la
        # page liste la tâche entrée
        # "1: Rendre grâce au Créateur"
        # en tant qu'élément d'une liste à puces
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table("1: Rendre grâce au Créateur")

        # il y a toujours le champ qui permet d'insérer des tâches. Bill va
        # donc saisir une deuxième tâche. Il entre "Se laver"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Se laver')
        inputbox.send_keys(Keys.ENTER)

        # la page se raffraichit et montre maintenant les deux items sur la
        # page
        self.check_for_row_in_list_table("1: Rendre grâce au Créateur")
        self.check_for_row_in_list_table("2: Se laver")


if __name__ == '__main__':
    unittest.main(warnings='ignore')
