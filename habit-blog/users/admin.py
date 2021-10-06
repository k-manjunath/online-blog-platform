from django.contrib import admin


from .models import User
from django.contrib.auth.admin import UserAdmin #used as helper class for admin screens

# Register your models here.
#admin.site.register(User)

class UsersAdmin(UserAdmin):
    '''What details admin can see on admin panel'''
    list_display = ['email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff']

    '''The attribures that can be used by admin in order to search a particular user'''
    search_fields = ['email', 'username']
    
    #pretty self explanatory
    readonly_fields = ['date_joined','last_login']

    #unclear - throws errors if not declared
    filter_horizontal = []
    list_filter = []
    fieldsets = []

admin.site.register(User, UsersAdmin)