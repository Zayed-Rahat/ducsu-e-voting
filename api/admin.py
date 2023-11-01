from django.contrib import admin
from .models import *
# Register your models here.


class ElectionAdmin(admin.ModelAdmin):
    list_display =['title','start_date', 'end_date', 'admin', 'is_open']
    list_filter = ['title']
    search_fields = ['title']

admin.site.register(Election)
admin.site.register(Voter)
admin.site.register(Position)
admin.site.register(Candidate)
admin.site.register(Vote)
admin.site.register(ContactMessage)