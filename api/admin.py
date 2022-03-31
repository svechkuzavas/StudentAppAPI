from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(UserProfile, admin.ModelAdmin)
admin.site.register(Article, admin.ModelAdmin)
admin.site.register(Reference, admin.ModelAdmin)