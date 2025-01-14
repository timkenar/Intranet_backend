from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from simple_history.admin import SimpleHistoryAdmin

from .models import Role, UserRole, History, UserInvitation

from django import forms

class UserRoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = ['role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget = forms.RadioSelect()
        self.fields['role'].queryset = Role.objects.all()

class UserRoleInline(admin.TabularInline):
    model = UserRole
    form = UserRoleForm
    extra = 1
class UserRoleInline(admin.TabularInline):
    model = UserRole
    extra = 1

class UserAdmin(BaseUserAdmin):
    inlines = (UserRoleInline,)

class HistoryAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')


admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(History)
admin.site.register(UserInvitation)
