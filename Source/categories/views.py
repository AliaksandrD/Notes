from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.views import generic
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
    template_name = 'categories/category_form.html'
    form_class = forms.CategoryForm
    redirect_field_name = 'category:by_category'

    def form_valid(self, form):
        name = form.cleaned_data['name']

        models.Category.objects.create(name=name, user=self.request.user)
        return HttpResponseRedirect(reverse('category:all'))


class CreateNote(LoginRequiredMixin, generic.CreateView):
    template_name = 'categories/note_form.html'
    form_class = forms.NoteForm

    def form_valid(self, form):
        name = form.cleaned_data['name']
        text = form.cleaned_data['message']
        password = form.cleaned_data['password']

        category = models.Category.objects.filter(
            slug=self.kwargs.get("slug"), pk=self.kwargs.get('pk')).get()

        encr = hexlify(encrypt(str(password), str(text)))

        models.Note.objects.create(name=name, password='0',
                                   message=encr, category=category, user=self.request.user)

        return HttpResponseRedirect(reverse('category:by_category', kwargs={'slug': category.slug, 'pk': category.pk}))


class ListCategory(LoginRequiredMixin, generic.ListView):
    model = models.Category

    def get_queryset(self):
        return models.Category.objects.filter(user=self.request.user)


class UserNotes(LoginRequiredMixin, generic.ListView):
    model = models.Note
    template_name = "categories/note_list.html"

    def get_queryset(self):
        self.category = get_object_or_404(
            models.Category, slug=self.kwargs['slug'], pk=self.kwargs['pk'])
        First = models.Note.objects.filter(
            category=self.category, user=self.request.user)
        my_set = [First, self.category]
        return my_set


class NotesDetail(LoginRequiredMixin, generic.DetailView):
    model = models.Note
    template_name = 'categories/note_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)


class Decrpt(LoginRequiredMixin, generic.UpdateView):
    template_name = 'categories/note_detail.html'
    model = models.Note
    fields = ['password']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = {}
        password = request.POST.get('password')
        message = request.POST.get('message')
        context['note'] = self.object
        checkbox = request.POST.get('encrypted')

        if checkbox == '1':  # checks if form for decoding
            try:  # try to decode message
                context['message'] = decrypt(password, unhexlify(
                    self.object.message[2:-1])).decode('utf-8')
            except DecryptionException:  # if wrong password return to detail note page
                return render(request, 'categories/note_detail.html', context=context)

            else:
                return render(request, 'categories/note_detail.html', context=context)

        else:  # if form for decryption-> change meessage-> save()
            self.object.message = hexlify(encrypt(str(password), str(message)))
            self.object.save()
            return render(request, 'categories/note_detail.html', context=context)


class NoteDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Note
    select_related = ("user", "note")
    success_url = reverse_lazy("category:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)


class CategoryDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Category
    select_related = ("user", "category")
    success_url = reverse_lazy("category:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)
