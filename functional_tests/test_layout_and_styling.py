# from django.test import LiveServerTestCase
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Bill se rend sur la page d'accueil et redimensionne la page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Il remarque que le champ d'entrée est bien centré
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # il saisit une tâche et voit que la boite est également centrée sur
        # la page permettant de gérer sa liste
        inputbox.send_keys('ceci est un test\n')
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )


# ceci n'est plus utile puisque l'on utilise LiveServerTestCase et que le test
# est chargé comme un module
if __name__ == '__main__':
    unittest.main(warnings='ignore')
