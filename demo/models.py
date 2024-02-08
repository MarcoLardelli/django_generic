from django.db import models
import sys, inspect


# abstract base class for generic models
class GenericBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    HAS_VIEW_URL = False # generate no link to view object by default

    NAME = "Please overwrite the NAME property of all generic classes!"

    class Meta:
        abstract=True # Set this model as Abstract



# Create your models here. subclass from GenericBase base model

class Author(GenericBase):

    NAME = "Author"

    name = models.CharField(max_length=100, verbose_name="First, second name")
    date_of_birth = models.DateField(verbose_name="Birth date")

    def __str__(self):
        return self.name
    

class Publisher(GenericBase):

    NAME = "Publisher"

    name = models.CharField(max_length=100, verbose_name="Name")

    def __str__(self):
        return self.name


class Book(GenericBase):

    NAME = "Book"

    HAS_VIEW_URL = True  # this one needs a view url (which is included into the list view)

    name = models.CharField(max_length=100, verbose_name="Book title")
    description = models.CharField(max_length=500, verbose_name="Description")

    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher,on_delete=models.CASCADE)

    def __str__(self):
        return self.name+" (by "+self.author.name+")"
    


cls_members = inspect.getmembers(sys.modules[__name__], inspect.isclass)

GENERIC_CLASSES = []
for cls in cls_members:
    if issubclass(cls[1],GenericBase) and (not cls[1].__name__=='GenericBase'):
        GENERIC_CLASSES.append(cls[1])





