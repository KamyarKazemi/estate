from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    readonly_fields = ('last_login', 'date_joined')

    list_display = ('phone_number', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')

    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

    search_fields = ('phone_number', 'email', 'first_name', 'last_name')

    ordering = ('phone_number',)

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('personal information', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('important date', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'phone_number', 'email', 'first_name', 'last_name', 'role',
                'password', 'confirm_password'
            ),
        }),
    )
