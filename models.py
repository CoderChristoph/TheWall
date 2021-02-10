from __future__ import unicode_literals
from django.db import models

import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        # First Name Validation
        if len(postData['f_name']) < 1:
            errors['first_name'] = "First Name is a Required Field!"
        elif len(postData['f_name']) < 2:
            errors['first_name'] = "First name must have 2 or more characters"
        elif postData['f_name'].isalpha() == False:
            errors['first_name'] = "First name must only contain letters!"

        # Last Name Validation
        if len(postData['l_name']) < 1:
            errors['last_name'] = 'Last name is a Required Field!'
        elif len(postData['l_name']) < 2:
            errors['last_name'] = "Last name must have 2 or more characters"
        elif postData['l_name'].isalpha() == False:
            errors['last_name'] = "Last name must only contain letters!"

        # Email Validation
        if len(postData['email']) < 1:
            errors['email'] = "Email is a Required Field!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email!"
        existing_users = User.objects.filter(email=postData['email'])
        if len(existing_users) > 0:
            errors['email'] = "That email already exists!"

        # Password Validation
        if len(postData['pw']) < 1:
            errors['pw'] = "Password is a Required Field"
        elif len(postData['pw']) < 8:
            errors['pw'] = "The password must contain 8 characters or more!"
        else:
            if postData['pw'] != postData['cpw']:
                errors['cw'] = "The passwords do not match!"

        return errors

    def login_validator(self, postData):
        errors = {}
        # Email Validation
        if len(postData['LEmail']) < 1:
            errors['email'] = "Email is a Required Field!"
        elif not EMAIL_REGEX.match(postData['LEmail']):
            errors['email'] = "Invalid Email!"

        # Password Validation
        if len(postData['LPassword']) < 1:
            errors['pw'] = "Password is a Required Field"
        elif len(postData['LPassword']) < 8:
            errors['pw'] = "The password must contain 8 characters or more!"



        return errors


class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw = models.CharField(max_length=255)
    objects = UserManager()


class Message(models.Model):
    newmessage = models.TextField()
    user = models.ForeignKey(User, related_name="user_messages")
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    newcomment = models.TextField()
    user = models.ForeignKey(User, related_name="user_comments")
    message = models.ForeignKey(Message, related_name="message_comments")
    created_at = models.DateTimeField(auto_now_add=True)


