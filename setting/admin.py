from django.contrib import admin
from .models import Setting, Contact
# Register your models here.


class SettingsAdmin(admin.ModelAdmin):
    list_display = (
        'phone_number',
        'email',
        'address',
    )


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'name',
        'subject'
    )
    search_fields = ('email', 'name')


admin.site.register(Setting, SettingsAdmin)
admin.site.register(Contact, ContactAdmin)
