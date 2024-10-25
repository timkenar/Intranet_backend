# license/admin.py

from django.contrib import admin
from .models import Subscription, License

from django.contrib import admin
from .models import Subscription, License, UserGroup

class LicenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'subscription', 'start_date', 'end_date', 'is_active')
    list_filter = ('subscription', 'is_active', 'group')
    search_fields = ('user__username', 'group__name')

admin.site.register(Subscription)
admin.site.register(UserGroup)
admin.site.register(License, LicenseAdmin)

