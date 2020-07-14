from django.contrib import admin

from url_shortener.models import UrlStore


class UrlStoreAdmin(admin.ModelAdmin):
    model = UrlStore
    list_display = ['user_url', 'url_hash']
    list_per_page = 25
    search_fields=('user_url',)
    list_filter=('user_url',)


admin.site.register(UrlStore, UrlStoreAdmin)
