from django import forms
from . import models

class CategoryForm(forms.ModelForm):
    class Meta:
        model=models.Categories
        fields=['name']


class NotesForm(forms.ModelForm):
    class Meta:
        model = models.Notes
        fields=['name','message','password']


