from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect


class HomePage(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("logged_in"))
        return super().get(request, *args, **kwargs)


class LoggedIn(TemplateView):
    template_name = 'logged_in.html'


class ThanksPage(TemplateView):
    template_name = 'thanks.html'
