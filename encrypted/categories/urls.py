from django.urls import path,include
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.ListCategory.as_view(), name="all"),
    path("new/", views.CreateCategory.as_view(), name="create"),
    path("notes/in/<slug>/",views.UserNotes.as_view(),name="by_category"),
    path("new/notes/in/<slug>/",views.CreateNote.as_view(),name="new_note"),
    path('notes/detail/<pk>',views.NotesDetail.as_view(),name='notes_detail'),
    path('notes/decrypt/<pk>', views.Decrpt.as_view(),name='decrypt'),
    path('delete/<pk>/', views.NoteDelete.as_view(),name='delete_note')

   
]
