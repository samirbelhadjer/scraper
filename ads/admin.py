from django.contrib import admin
from .models import Ad


class AdsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','position',
                    'is_active')
    list_display_links = ('id', 'title',)
    search_fields = ('title',)
    list_filter = ('is_active', 'position')
    list_per_page = 100
    list_editable = ('is_active',)

admin.site.register(Ad, AdsAdmin)
