from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'mobile_phone', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('mobile_phone',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('email', 'first_name', 'last_name', 'mobile_phone')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
