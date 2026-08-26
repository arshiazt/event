from django.contrib import admin
from registration.models import Registration

# Register your models here.

class RegistrationAdmin(admin.ModelAdmin):
    
    list_display = ('user','event','status')
    readonly_fields = ('created_at','canceled_at')
    search_fields = ('user',)
    list_filter = ('user','status')

admin.site.register(Registration,RegistrationAdmin)