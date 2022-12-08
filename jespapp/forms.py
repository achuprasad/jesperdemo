from django import forms

from jespapp.models import Person


class PersonForm(forms.ModelForm):
    class Meta:
        model=Person
        fields=('email','password')