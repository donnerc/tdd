from django.shortcuts import render, redirect
from lists.models import Item, List

from django.core.exceptions import ValidationError


# Create your views here.
def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    if request.method == 'POST':
        list_ = List.objects.create()
        item = Item(text=request.POST['item_text'], list=list_)
        try:
            item.full_clean()
            item.save()
        except ValidationError:
            list_.delete()
            error = 'Impossible de créer une liste avec un item qui est vide'
            return render(request, 'home.html', {'error': error})
        return redirect('/lists/{}/'.format(list_.id))


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/{}/'.format(list_.id))