from django.core.exceptions import ValidationError
from library_api.models import Books
from datetime import datetime

def validate_title_is_unique(title):
    if Books.objects.filter(title=title).exists():
        raise  ValidationError("title is already present in database!")

def validate_isbn_is_unique(isbn):
    # if null pass
    if isbn is not None :
        
        if Books.objects.filter(isbn=isbn).exists():
            raise  ValidationError("isbn is already present in database!")

def validate_isbn(isbn):
    # if null pass
    if isbn is not None :
        if len(isbn) >13:
            ValidationError("isbn is too long!")
        elif len(isbn) < 10:
            ValidationError("isbn is too short!")


