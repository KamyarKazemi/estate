from django.contrib import admin
from .models import Agency



@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    """showing fields in main menu"""
    list_display = ('agent' , 'name' , 'license_number' , 'is_verified')

    """filtering items and clicking"""
    search_fields = ('name' , 'license_number' , 'is_verified')
    list_filter = ('name' , 'license_number' , 'business_phone' , 'agent__phone_number')

    """ordering by """
    ordering = ('-created',)


