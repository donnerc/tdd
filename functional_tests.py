from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # demande à Selenium d'attendre 3 secondes si nécessaire (chargement
        # de la page) avant de faire les tests
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Bill a entendu parler d'un nouveau site permettant de gérer ses
        # tâches. Il se dépeche de visiter le site de développement
        self.browser.get('https://tdd-c9-donnerc.c9.io/')

        # il remarque que la page a un titre qui contient le mot 'To-Do'
        self.assertIn('To-Do', self.browser.title)
        self.fail('il ne faut pas oublier de terminer ce test')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
