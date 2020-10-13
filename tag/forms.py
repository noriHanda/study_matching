from django import forms
from offer.models import Offer


class TagChangeListForm(forms.ModelForm):
    # here we only need to define the field we want to be editable
    offer = forms.ModelMultipleChoiceField(
        queryset=Offer.objects.all(), required=False)