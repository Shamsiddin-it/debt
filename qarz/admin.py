from .models import *
from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ['username', 'email', 'is_staff', 'is_active']
#     # Add any other fields or configurations needed

# admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Debt)