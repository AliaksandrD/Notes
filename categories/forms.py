from django import forms
from . import models

class CategoryForm(forms.ModelForm):
    class Meta:
        model=models.Category
        fields=['name']


class NoteForm(forms.ModelForm):
    class Meta:
        model = models.Note
        fields=['name','message','password']


