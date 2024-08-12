from django.contrib import admin
from .models import Department, CustomUser

# Register your models here.

admin.site.register(Department)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id','first_name', 'last_name', 'status', 'DeptId')
    search_fields = ('username','id', 'email')
    list_filter = ('status', 'DeptId')