from django.contrib import admin

from url_shortener.models import Url


class UrlAdmin(admin.ModelAdmin):
    model = Url
    list_display = ['user_url', 'url_hash']


admin.site.register(Url, UrlAdmin)
