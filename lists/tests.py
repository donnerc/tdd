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

        home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new todo item')

        # je ne suis pas sur que ce code doive ici, il n'indiquait pas où le
        # mettre ... ce code n'a plus de sens avec la redirection

        # self.assertIn('new todo item', response.content.decode())
        # expected_html = render_to_string(
        #     'home.html',
        #     {'new_item_text' : 'new todo item'}
        # )
        # self.assertEqual(response.content.decode(), expected_html)

        # vérifie que l'on soit bien redirigé ...

    def test_home_redirects_after_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'new todo item'

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

    def test_home_page_only_saves_items_on_post_request(self):
        request = HttpRequest()
        home_page(request)

        self.assertEqual(Item.objects.count(), 0)


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


class ListViewTest(TestCase):

    def test_display_all_items(self):
        Item.objects.create(text='premier item')
        Item.objects.create(text='deuxième item')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'premier item')
        self.assertContains(response, 'deuxième item')

    def test_uses_list_templates(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')
