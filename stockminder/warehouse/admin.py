from django.contrib import admin
from .models import Department, CustomUser

# Register your models here.

admin.site.register(Department)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'status', 'registerDate', 'DeptId')
    search_fields = ('username', 'first_name', 'last_name', 'status')
    list_filter = ('status', 'DeptId')