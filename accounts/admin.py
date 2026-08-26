from django.contrib import admin
from accounts.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    
    list_display = ('phone','participant','organizer','is_active','is_superuser')
    list_filter = ('participant','is_superuser')
    empty_value_display = "-empty-"
    readonly_fields = ('created_date','updated_date')
    fields = ('phone','participant','organizer','is_active','is_staff','is_superuser','created_date','updated_date','password')
    search_fields = ('phone',)
    
admin.site.register(User,UserAdmin)