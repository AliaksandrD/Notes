from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from simplecrypt import encrypt, decrypt, DecryptionException
from binascii import hexlify, unhexlify
from . import models, forms
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.


class CreateCategory(LoginRequiredMixin, generic.CreateView):
    template_name = 'category/category_form.html'
    form_class = forms.CategoryForm
    redirect_field_name = 'category:by_category'

    def form_valid(self, form):
        name = form.cleaned_data['name']

        models.Category.objects.create(name=name, user=self.request.user)
        return HttpResponseRedirect(reverse('category:all'))


class CreateNote(LoginRequiredMixin, generic.CreateView):
    template_name = 'category/note_form.html'
    form_class = forms.NoteForm

    def form_valid(self, form):
        name = form.cleaned_data['name']
        text = form.cleaned_data['message']
        password = form.cleaned_data['password']

        category = models.Category.objects.filter(
            slug=self.kwargs.get("slug"), pk=self.kwargs.get('pk')).get()

        encr = hexlify(encrypt(str(password), str(text)))

        models.Note.objects.create(name=name, password='0', encrypted=True,
                                   message=encr, category=category, user=self.request.user)

        return HttpResponseRedirect(reverse('category:by_category', kwargs={'slug': category.slug, 'pk': category.pk}))


class ListCategory(LoginRequiredMixin, generic.ListView):

    model = models.Category

    def get_queryset(self):
        return models.Category.objects.filter(user=self.request.user)


class UserNotes(LoginRequiredMixin, generic.ListView):
    model = models.Note
    template_name = "category/note_list.html"

    def get_queryset(self):
        self.category = get_object_or_404(
            models.Category, slug=self.kwargs['slug'], pk=self.kwargs['pk'])
        First = models.Note.objects.filter(
            category=self.category, user=self.request.user)
        my_set = [First, self.category]
        return my_set


class NotesDetail(LoginRequiredMixin, generic.DetailView):
    model = models.Note
    template_name = 'category/note_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)


class Decrpt(LoginRequiredMixin, generic.UpdateView):
    template_name = 'category/note_detail.html'
    model = models.Note
    fields = ['password']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        password = request.POST.get('password')
        message = request.POST.get('message')
        print(self.object.encrypted)
        if self.object.encrypted:
            try:
                self.object.message = decrypt(password, unhexlify(
                    self.object.message[2:-1])).decode('utf-8')
                self.object.encrypted = False
                self.object.save()
            except DecryptionException:
                messages.warning(self.request, ("Wrong Password"))

            else:
                messages.success(self.request, "Encrypted")

        else:
            self.object.message = hexlify(encrypt(str(password), str(message)))
            self.object.encrypted = True
            self.object.edit()
            self.object.save()

        return HttpResponseRedirect(reverse('category:note_detail',
                                            kwargs={'pk': self.object.pk}))


class NoteDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Note
    select_related = ("user", "note")
    success_url = reverse_lazy("category:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Note Deleted")
        return super().delete(*args, **kwargs)
