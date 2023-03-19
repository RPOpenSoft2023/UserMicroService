from django.contrib import admin


from .models import *
class Useradmin(admin.ModelAdmin):
    list_display=('first_name','email')
# Register your models here.
admin.site.register(UserAPI,Useradmin)