from email.policy import default
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
'''whenever a custom user model is created, it is recommended to create a user manager model too'''

class MyAccountManager(BaseUserManager):
    '''email,username,first_name are required so are taken as parameters'''
    def create_user(self, email, username, first_name, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not username:
            raise ValueError("User must have an username")
        if not first_name:
            raise ValueError("Please provide your first name")
        user = self.model(
                email = self.normalize_email(email),
                username = username,
                first_name = first_name,
        )

        user.set_password(password) #mistake: user.set_password = password
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username,first_name, password):
        user = self.create_user(
                email = self.normalize_email(email),
                username = username,
                first_name = first_name,
                password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    first_name = models.CharField(verbose_name='first_name', max_length=60)
    last_name = models.CharField(verbose_name='last_name', max_length=60)
    username = models.CharField(max_length=30, unique=True)

    #required for custom user model
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)   #auto_now_add - adds only once when created
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True) #auto_now - adds whenever logged in
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    '''(this is a keyword)deafult value: username (required at time of login) 
        By setting it to email django takes in email address instead of username for login'''
    USERNAME_FIELD = 'email'

    '''a list fields that MUST be filled in order to register'''
    REQUIRED_FIELDS = ['username', 'first_name']
    
    '''Provides the info about where the manager is and how to use it'''
    objects = MyAccountManager()

    '''dunder str method: whenever a instance of this class is created that instance will be displayed/rendered with what this method will be returning(generally observed in admin panel)'''
    def __str__(self):
        return self.username
    
    #methods required for custom user object creation
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    