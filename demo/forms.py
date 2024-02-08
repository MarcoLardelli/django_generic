from django.forms import ModelForm

from .models import Author, Publisher, Book, GENERIC_CLASSES


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        exclude = ()


class PublisherForm(ModelForm):
    class Meta:
        model = Publisher
        exclude = ()

class BookForm(ModelForm):
    class Meta:
        model = Book
        exclude = ()


GENERIC_CLASSES_AND_FORMS = []
for cl in GENERIC_CLASSES:
    form_cl = globals()[cl.__name__+"Form"]
    GENERIC_CLASSES_AND_FORMS.append((cl,form_cl))