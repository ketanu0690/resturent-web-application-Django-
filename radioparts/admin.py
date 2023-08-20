from django.contrib import admin
from .models import RadioPart

@admin.register(RadioPart)
class RadioPartAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'availability', 'image')  # Display image in admin list
