from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime
from time import strftime, localtime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')

class UserManager(models.Manager):
    def login(self, post):
        users = self.filter(email = post['email'].lower())
        if len(users):
            user = users[0]
            if bcrypt.checkpw(post['password'].encode(), user.password.encode()):
                return user

        return False

    def validate(self, post):
        errors = {}

        for key, val in post.items():
            if len(val) < 1:
                errors[key] = '{} cannot be empty'.format(key.replace('_',' ').title())

        if 'first_name' not in errors and not post['first_name'].isalpha():
            errors['first_name'] = 'First name should contain only alphabets'

        if 'last_name' not in errors and not post['last_name'].isalpha():
            errors['last_name'] = 'Last name should contain only alphabets'

        if 'email' not in errors and not re.match(EMAIL_REGEX, post['email'].lower()):
            errors['email'] = 'Invalid email address entered'

        if 'birthday' not in errors and post['birthday'] > strftime("%Y-%m-%d", localtime()):
            errors['birthday'] = 'Invalid birth date entered'

        if 'password' not in errors and (len(post['password']) < 8 or not re.match(PASSWORD_REGEX, post['password'])):
            errors['password'] = 'Password must be at least 8 characters and contain a digit and capital letter'
        elif 'password' not in errors and post['password'] != post['password_confirmation']:
            errors['password'] = 'Passwords do not match'

        if not len(errors.keys()):
            if len(self.filter(email = post['email'].lower())) > 0:
                errors['email'] = 'Email address already in use'

        return errors
    
    def createUser(self, post):
        return self.create(
            first_name = post['first_name'],
            last_name = post['last_name'],
            email = post['email'].lower(),
            password = bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt()),
            birthday = post['birthday']
        )
    


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255)
    password = models.CharField(max_length = 255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
