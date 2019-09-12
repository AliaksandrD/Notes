from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse,reverse_lazy
from django.http import Http404,HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from simplecrypt import encrypt,decrypt,DecryptionException
from binascii import hexlify, unhexlify
from . import models,forms
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.


class CreateCategory(LoginRequiredMixin,generic.CreateView):
    template_name='categories/categories_form.html'
    form_class=forms.CategoryForm
    redirect_field_name ='categories:by_category'
    
    def form_valid(self,form):

        name=form.cleaned_data['name']

        if not models.Categories.objects.filter(name=name).exists():
            models.Categories.objects.create(name=name)
        category=models.Categories.objects.filter(name=name).get()
        try:
            models.UserCategory.objects.create(user=self.request.user,category=category)

        except IntegrityError:
            messages.warning(self.request,("Warning, you already have category".format(category.name)))

        else:
            messages.success(self.request,"Category {} created.".format(category.name))
        
        return HttpResponseRedirect(reverse('categories:all'))


class CreateNote(LoginRequiredMixin,generic.CreateView):
    template_name='categories/notes_form.html'
    form_class=forms.NotesForm
   
    

    def form_valid(self, form):
        name=form.cleaned_data['name']
        text=form.cleaned_data['message']
        password=form.cleaned_data['password']
       
        category=models.Categories.objects.filter(
                slug=self.kwargs.get("slug")).get()
        if not models.Notes.objects.filter(name=name, user=self.request.user ).exists():
            
            encr=hexlify(encrypt(str(password),str(text)))
          
            models.Notes.objects.create(name=name, password='0', encrypted=True, message=encr, category=category, user= self.request.user) 
            
            
        
        return HttpResponseRedirect(reverse('categories:by_category', kwargs={'slug':category.slug}))


class ListCategory(LoginRequiredMixin,generic.ListView):

    model = models.UserCategory
   


class UserNotes(LoginRequiredMixin,generic.ListView):
    model = models.Notes
    template_name = "categories/notes_list.html"
    def get_queryset(self):
        self.category=get_object_or_404(models.Categories, slug=self.kwargs['slug'])
        return models.Notes.objects.filter(category=self.category, user=self.request.user)

    

class NotesDetail(LoginRequiredMixin,generic.DetailView):
    model=models.Notes
    template_name='categories/notes_detail.html'




class Decrpt(LoginRequiredMixin,generic.UpdateView):
    template_name='categories/notes_detail.html'
    model=models.Notes
    fields = ['password']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        password=request.POST.get('password')
        message=request.POST.get('message')
        print(self.object.encrypted)
        if self.object.encrypted:
            try:
                self.object.message=decrypt(password,unhexlify(self.object.message[2:-1])).decode('utf-8')
                self.object.encrypted=False
                self.object.save()
            except DecryptionException:
                messages.warning(self.request,("Wrong Password"))

            else:
                messages.success(self.request,"Encrypted")
                
            
        else:
            self.object.message=hexlify(encrypt(str(password),str(message)))
            self.object.encrypted=True
            self.object.save()
        
        return HttpResponseRedirect(reverse('categories:notes_detail',
                            kwargs={'pk': self.object.pk})) 
    

class NoteDelete(LoginRequiredMixin,generic.DeleteView):
    model = models.Notes
    select_related = ("user", "notes")
    success_url = reverse_lazy("categories:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Note Deleted")
        return super().delete(*args, **kwargs)  

