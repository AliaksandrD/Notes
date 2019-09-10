from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
# Create your models here.
User=get_user_model()


class Categories(models.Model):
    name=models.CharField(max_length=50, unique=True)
    slug=models.SlugField(allow_unicode=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    notes = models.ForeignKey(Notes, on_delete=models.PROTECT, related_name="notes",null=True, blank=True)
 
    def get_absolute_url(self):
        return reverse("categories_list")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ["name"]