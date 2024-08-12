from django.contrib import admin
from .models import Department, CustomUser, Category, Item, Vendor

# Register your models here.

admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Vendor)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id','first_name', 'last_name', 'status', 'DeptId')
    search_fields = ('username','id', 'email')
    list_filter = ('status', 'DeptId')