from django.contrib import admin
from feedback.models import *

# Register your models here.

class RatingAdmin(admin.ModelAdmin):

    list_display = ('user','event')
    fields = ('user','event','value')
    search_fields =  ('event',)
    readonly_fields = ('user','event','value')

class CommentAdmin(admin.ModelAdmin):

    list_display = ('user','event')
    fields = ('user','event','text')
    search_fields =  ('event',)
    readonly_fields = ('user','event','text')

admin.site.register(EventComment,CommentAdmin)
admin.site.register(EventRating,RatingAdmin)