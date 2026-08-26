from django.contrib import admin
from event.models import *

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    
    list_display = ('title','owner','status','published_date')
    search_fields = ('title','owner')
    readonly_fields = ('owner','created_date','updated_date')
    fields = ('title','owner','capacity','status','published_date','start_date','end_date')

class AttributeAdmin(admin.ModelAdmin):

    list_display = ('name','value_type',)
    search_fields = ('name',)

admin.site.register(Event,EventAdmin)
admin.site.register(Attribute,AttributeAdmin)
admin.site.register(EventAttributeValue)