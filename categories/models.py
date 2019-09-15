from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
# Create your models here.
User=get_user_model()


class Category(models.Model):
    name=models.CharField(max_length=50)
    slug=models.SlugField(allow_unicode=True)
    user = models.ManyToManyField(User,through="UserCategory")
    
 
    def get_absolute_url(self):
        return reverse("categories:single", kwargs={'slug': self.slug})

    def __str__(self):
        return self.name 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ["name"]


class Note(models.Model):
    name=models.CharField(max_length=50, blank=False)
    
    created_at = models.DateTimeField(auto_now=True)
   
    message = models.TextField()
    password=models.CharField(max_length=100,blank=False)
    encrypted=models.BooleanField(default=False)
    user = models.ForeignKey(User,related_name='user_notes',on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="notes_cat",blank=False)

    def __str__(self):
        return self.name

    def edit(self):
        self.edited_at=timezone.now()
        self.save()
   


    def get_absolute_url(self):
        return reverse("categories:note", kwargs={'username':self.user.username, 'pk':self.pk})
    
    class Meta:
        ordering=['-created_at']


class UserCategory(models.Model):
    
    category = models.ForeignKey(Category,related_name='category_notes',on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='user_category',on_delete=models.CASCADE)
    
    
    
    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ["user",'category']




