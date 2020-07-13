import logging

from django.shortcuts import render
from django.views import View

from url_shortener.forms import UrlForm
from url_shortener.models import Url

logger = logging.getLogger(__name__)


class UrlView(View):

    def get(self, request, *args, **kwargs):
        form = UrlForm()
        context = {'form': form}
        return render(request, 'url_form.html', context)

    def post(self, request, *args, **kwargs):
        form = UrlForm(data=request.POST)
        if form.is_valid():
            url, _ = Url.objects.get_or_create(user_url=form.cleaned_data['user_url'])
            short_url = url.get_short_url(request)
            render(request, 'url_form.html', {'form': form, 'short_url': short_url})
            return render(request, 'url_form.html', {'form': form, 'short_url': short_url})
        return render(request, 'url_form.html', {'form': form})
