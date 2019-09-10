from django.db import models
from django.utils import timezone
from categories.models import Categories
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
class Notes(models.Model):
    name=models.CharField(max_length=50)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="notes")
    created_at = models.DateTimeField(auto_now=True)
    edited_at = models.DateTimeField(blank=True, null=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    encrypted=models.BooleanField(default=False)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE ,related_name="categories",null=True, blank=True)

    def __str__(self):
        return self.name

    def edit(self):
        self.edited_at=timezone.now()
        self.save()

    def encrypt(self):
        self.encrypted=True
        self.save()

    def decrypt(self):
        self.encrypted=False
        self.save

    def get_absolute_url(self):
        return reverse("notes_list")
    
