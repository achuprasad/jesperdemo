from django import forms

from jespapp.models import Person, Documents


class PersonForm(forms.ModelForm):
    class Meta:
        model=Person
        fields=('email','password')


class DocumentForm(forms.Form):

    firstname = forms.CharField(label='firstname', max_length=200)
    middlename = forms.CharField(label='middlename', max_length=100)
    lastname = forms.CharField(label='lastname', max_length=100)
    address = forms.CharField(label='address', max_length=250)
    pincode = forms.IntegerField()
