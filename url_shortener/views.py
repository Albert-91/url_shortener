import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View

from url_shortener.forms import UrlStoreForm
from url_shortener.models import UrlStore

logger = logging.getLogger(__name__)


class UrlView(View):

    def get(self, request, *args, **kwargs):
        form = UrlStoreForm()
        context = {'form': form}
        return render(request, 'url_form.html', context)

    def post(self, request, *args, **kwargs):
        form = UrlStoreForm(data=request.POST)
        if form.is_valid():
            url, _ = UrlStore.objects.get_or_create(user_url=form.cleaned_data['user_url'])
            short_url = url.get_short_url(request)
            return render(request, 'url_form.html', {'form': form, 'short_url': short_url, 'url': url})
        return render(request, 'url_form.html', {'form': form})


class UrlRedirectView(View):

    def get(self, request, url_hash=None, *args, **kwargs):
        obj = get_object_or_404(UrlStore, url_hash=url_hash)
        return HttpResponseRedirect(obj.user_url)
