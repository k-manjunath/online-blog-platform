from django.contrib import admin

from .models import Habit, Post

# Register your models here.
class Habits(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_created']
    search_fields = ['title', 'author']
    ordering = ['-date_created']

class Posts(admin.ModelAdmin):
    list_display = ['title', 'habit', 'author', 'date_posted']
    search_fields = ['title', 'habit', 'author']
    ordering = ['-date_posted']


admin.site.register(Habit, Habits)
admin.site.register(Post, Posts)