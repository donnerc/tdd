from django.test import TestCase
from lists.models import Item, List

from django.core.exceptions import ValidationError

class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        item1 = Item()
        item1.text = "Mon premier item dans la liste"
        item1.list = list_
        item1.save()

        item2 = Item()
        item2.text = "Deuxième item"
        item2.list = list_
        item2.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, "Mon premier item dans la liste")
        self.assertEqual(saved_items[0].list, list_)
        self.assertEqual(saved_items[1].text, "Deuxième item")
        self.assertEqual(saved_items[1].list, list_)

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        url = '/lists/{}/'.format(list_.id)
        self.assertEqual(list_.get_absolute_url(), url)