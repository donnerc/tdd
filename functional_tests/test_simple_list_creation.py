# from django.test import LiveServerTestCase
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Bill a entendu parler d'un nouveau site permettant de gérer ses
        # tâches. Il se dépeche de visiter le site de développement
        # self.browser.get('https://tdd-c9-donnerc.c9.io/')
        self.browser.get(self.live_server_url)

        # il remarque que la page a un titre et un en-têtequi contient le mot
        # 'To-Do'
        # wait = input('press any key to continue ...')
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # il voit qu'il y a un champ d'entrée de type texte dans lequel il
        # peut taper sa tâche
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Saisir votre tâche ici'
        )

        # il entre la première chose à faire le matin
        inputbox.send_keys('Rendre grâce au Créateur')

        # lorsqu'elle presse sur la touche ENTER, une nouvelle URL est générée
        # pour sa nouvelle liste contenant comme premier élément "1: Rendre
        # grâce au Créateur"
        inputbox.send_keys(Keys.ENTER)
        bill_list_url = self.browser.current_url
        self.assertRegex(bill_list_url, '/lists/.+')
        self.check_for_row_in_list_table("1: Rendre grâce au Créateur")

        # il y a toujours le champ qui permet d'insérer des tâches. Bill va
        # donc saisir une deuxième tâche. Il entre "Se laver"
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Se laver')
        inputbox.send_keys(Keys.ENTER)

        # la page se raffraichit et montre maintenant les deux items sur la
        # page
        self.check_for_row_in_list_table("1: Rendre grâce au Créateur")
        self.check_for_row_in_list_table("2: Se laver")

        # Cunéconde, la copine de Bill est impressionnée de la manière dont
        # Bill s'organise car il n'oublie plus de vider la poubelle. Elle
        # décide donc de se créer également une todo list.

        ## On utilise une nouvelle session pour s'assurer que
        ## Cunégonde n'arrive pas sur la liste de Bill
        self.browser.refresh()
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Cunégonde visite la page d'accueil et il n'y a aucune trace de la
        # liste de Bill
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Rendre grâce au Créateur', page_text)
        self.assertNotIn('Se laver', page_text)

        # Cunégonde commence une nouvelle liste en créant une première tâche
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Prendre une douche')
        inputbox.send_keys(Keys.ENTER)

        # Cunégonde reçoit une URL privée pour sa liste
        cunegonde_list_url = self.browser.current_url
        self.assertRegex(cunegonde_list_url, '/lists/.+')
        self.assertNotEqual(bill_list_url, cunegonde_list_url)

        # il n'y a toujours aucune trace de la liste de Bill
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Rendre grâce au Créateur', page_text)
        self.assertNotIn('Se laver', page_text)

        # tous deux satisfaits, ils partent joyeusement au travail


# ceci n'est plus utile puisque l'on utilise LiveServerTestCase et que le test
# est chargé comme un module
if __name__ == '__main__':
    unittest.main(warnings='ignore')
