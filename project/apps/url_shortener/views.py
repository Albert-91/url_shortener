import logging

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import FormView

from project.apps.url_shortener.forms import UrlStoreForm
from project.apps.url_shortener.models import UrlStore

logger = logging.getLogger(__name__)


class UrlView(FormView):

    template_name = 'url_form.html'
    form_class = UrlStoreForm

    def form_valid(self, form):
        url, is_created = UrlStore.objects.get_or_create(user_url=form.cleaned_data['user_url'])
        short_url = url.get_short_url()
        if is_created:
            logger.debug("Successfully saved provided URL: %s with hash value: %s" % (url, short_url))
        return self.render_to_response(
            context=self.get_context_data(short_url=short_url, url=url, is_created=is_created)
        )

    def get_success_url(self):
        return reverse('home')


class UrlRedirectView(View):

    def get(self, request, url_hash=None, *args, **kwargs):
        obj = get_object_or_404(UrlStore, url_hash=url_hash)
        return HttpResponseRedirect(obj.user_url)
