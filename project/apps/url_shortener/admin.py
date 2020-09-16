from django.contrib import admin
from django.utils.html import format_html

from url_shortener.models import UrlStore


class UrlStoreAdmin(admin.ModelAdmin):
    model = UrlStore
    list_display = ['user_url', 'url_hash', 'short_url']
    list_per_page = 25
    search_fields = 'user_url',
    list_filter = 'user_url',
    readonly_fields = 'short_url',

    def short_url(self, obj):
        return format_html('<a href="%s">%s</a>' % (obj.get_short_url(), obj.get_short_url()))

    short_url.allow_tags = True
    short_url.short_description = 'Short URL'


admin.site.register(UrlStore, UrlStoreAdmin)
