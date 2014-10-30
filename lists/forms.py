from django import forms
from lists.models import Item

EMPTY_LIST_ERROR = "Impossible de créer une liste avec un item qui est vide"

class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_LIST_ERROR}
        }


    # item_text = forms.CharField(
    #     widget=forms.fields.TextInput(attrs={
    #         'placeholder': 'Enter a to-do item',
    #         'class': 'form-control input-lg',
    #     }),
    # )
