from django.contrib import admin
from .models import Agency , AgencyAddress


class AgencyAddressInLine(admin.StackedInline):
    model = AgencyAddress
    can_delete = False
    verbose_name = "agency_address"
    verbose_name_plural = "agency_addresses"
    fk_name = "agency"

@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    inlines = [AgencyAddressInLine]
    """showing fields in main menu"""
    list_display = ('agent' , 'name' , 'license_number' , 'is_verified')

    """filtering items and clicking"""
    search_fields = ('name' , 'license_number' , 'is_verified')
    list_filter = ('name' , 'license_number' , 'business_phone' , 'agent__phone_number')

    """ordering by """
    ordering = ('-created',)

    @admin.display(description='province')
    def province_from_address(self, obj):
        address = getattr(obj, 'address', None)
        return address.province if address else "-"
