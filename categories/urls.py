from django.urls import path, include
from . import views

app_name = 'category'

urlpatterns = [
    path('', views.ListCategory.as_view(), name="all"),
    path("new/", views.CreateCategory.as_view(), name="create"),
    path("notes/in/<slug>/<pk>", views.UserNotes.as_view(), name="by_category"),
    path("notes/in/<slug>/<pk>/new", views.CreateNote.as_view(), name="new_note"),
    path('notes/detail/<pk>', views.NotesDetail.as_view(), name='note_detail'),
    path('notes/decrypt/<pk>', views.Decrpt.as_view(), name='decrypt'),
    path('delete/<pk>/', views.NoteDelete.as_view(), name='delete_note')


]
