from django.urls import path,include
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.ListCategory.as_view(), name="all"),
   
]
