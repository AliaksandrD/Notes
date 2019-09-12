from django.contrib import admin
from .models import Categories,Notes,UserCategory
# Register your models here.
admin.site.register(Categories)
admin.site.register(Notes)
admin.site.register(UserCategory)