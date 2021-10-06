from django.db import models
from django.utils import timezone

from users.models import User

from django.urls import reverse

# Create your models here.

class Habit(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    context = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    '''this method return a string(since reverse is used) as a route to the view(UserHabitCreateView in this case),
    Overall this method redirects us to the detail view of the habit created/updated after we submit the form'''
    def get_absolute_url(self):
        return reverse('detail-habit', kwargs={'pk':self.pk})
    


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=250)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('detail-habit', kwargs={'pk':self.habit.pk})
