from django.core.urlresolvers import resolve
from django.test import TestCase
from django.template.loader import render_to_string
from lists.views import home_page
from django.http import HttpRequest
from django.utils.html import escape

from lists.models import Item, List
from lists.forms import ItemForm

# test pour tester que les tests fonctionnent
# class SmokeTest(TestCase):
#     def test_bad_maths(self):
#         self.assertEqual(1 + 1, 3)


class HomePageTest(TestCase):

    maxDiff = None

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'text': 'new todo item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new todo item')

    def test_redirects_after_POST_request(self):
        response = self.client.post(
            '/lists/new',
            data={'text': 'new todo item'}
        )

        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/{}/'.format(new_list.id))

    def test_validation_errors_sent_back_to_homepage_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        # après une erreur, c'est de nouveau la page d'accueil qui se charge
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("Impossible de créer une liste avec un item qui est vide")
        self.assertContains(response, expected_error)

    def test_blank_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        response = self.client.get('/lists/{}/'.format(correct_list.id))
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='premier item', list=correct_list)
        Item.objects.create(text='deuxième item', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other premier item', list=other_list)
        Item.objects.create(text='other deuxième item', list=other_list)


        response = self.client.get('/lists/{}/'.format(correct_list.id))

        self.assertContains(response, 'premier item')
        self.assertContains(response, 'deuxième item')

        self.assertNotContains(response, 'other premier item')
        self.assertNotContains(response, 'other deuxième item')

    def test_uses_list_templates(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertTemplateUsed(response, 'list.html')

    def test_can_save_a_POST_request_to_existing_list(self):
        correct_list = List.objects.create()

        self.client.post(
            '/lists/{}/'.format(correct_list.id),
            data={'text': 'New ToDo item for existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'New ToDo item for existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/{}/'.format(correct_list.id),
            data={'text': 'New ToDo item for existing list'}
        )

        self.assertRedirects(response, '/lists/{}/'.format(correct_list.id))

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            '/lists/{}/'.format(list_.id),
            data={'text': ''}
        )
        self.assertEqual(response.status_code, 200)
        # après une erreur, c'est de nouveau la page d'accueil qui se charge
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("Impossible de créer une liste avec un item qui est vide")
        self.assertContains(response, expected_error)

    def test_blank_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)