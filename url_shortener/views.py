import logging

from django.db import transaction
from django.db.utils import DatabaseError
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
            try:
                with transaction.atomic():
                    Url.objects.create(user_url=form.cleaned_data['user_url'])
            except DatabaseError as e:
                logger.error(e)
            else:
                return render(request, 'url_form.html', {'form': form})
        return render(request, 'url_form.html', {'form': form})
