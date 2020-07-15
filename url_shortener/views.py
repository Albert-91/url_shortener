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
        ctx = {'form': form}
        if form.is_valid():
            url, _ = UrlStore.objects.get_or_create(user_url=form.cleaned_data['user_url'])
            logger.debug("Created %s" % url)
            short_url = url.get_short_url()
            logger.debug('Successfully hashed provided URL with value: %s' % short_url)
            ctx.update({'short_url': short_url, 'url': url})
            return render(request, 'url_form.html', ctx)
        return render(request, 'url_form.html', ctx)


class UrlRedirectView(View):

    def get(self, request, url_hash=None, *args, **kwargs):
        obj = get_object_or_404(UrlStore, url_hash=url_hash)
        return HttpResponseRedirect(obj.user_url)
