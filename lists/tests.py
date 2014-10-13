from django.core.urlresolvers import resolve
from django.test import TestCase
from django.template.loader import render_to_string
from lists.views import home_page
from django.http import HttpRequest

from lists.models import Item

# test pour tester que les tests fonctionnent
# class SmokeTest(TestCase):
#     def test_bad_maths(self):
#         self.assertEqual(1 + 1, 3)
        
        
class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
        
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)
    
    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'new todo item'
        
        response = home_page(request)
        
        self.assertIn('new todo item', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text' : 'new todo item'}
        )
        self.assertEqual(response.content.decode(), expected_html)
        
        
class ItemModelTest(TestCase):
    
    def test_saving_and_retrieving_items(self):
        item1 = Item()
        item1.text = "Mon premier item dans la liste"
        item1.save()
        
        item2 = Item()
        item2.text = "Deuxième item"
        item2.save()
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        self.assertEqual(saved_items[0].text, "Mon premier item dans la liste")
        self.assertEqual(saved_items[1].text, "Deuxième item")
        