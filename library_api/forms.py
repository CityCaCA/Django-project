
from django.forms import Form
from django import forms
from library_api.validators import validate_title_is_unique,validate_isbn_is_unique, validate_isbn

class BookCreationForm(Form):
        title = forms.CharField(max_length=100 , required=True, validators=[validate_title_is_unique])
        isbn = forms.CharField(max_length=100, validators=[validate_isbn,validate_isbn_is_unique])
        isbn13 = forms.CharField(required=False)
        author = forms.CharField(max_length=100, required=True)
        pub_year = forms.DateField(required=False, widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
        image_url = forms.CharField(max_length=200, required=False)
        lang_code = forms.CharField(max_length=20,required=False)

class BookUpdateForm(Form):
        isbn13 = forms.FloatField(required=False)
        author = forms.CharField(max_length=100, required=True)
        pub_year = forms.DateField(required=False, widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
        image_url = forms.CharField(max_length=200, required=False)
        lang_code = forms.CharField(max_length=20,required=False)
        