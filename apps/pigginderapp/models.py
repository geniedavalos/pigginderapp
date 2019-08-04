from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
from datetime import datetime

PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])+(?=.*[0-9])+.{8,40}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) == 0:
            errors['first_name'] = 'First Name cannot be empty'
        elif(len(postData['first_name'])) < 2:
            errors['first_name'] = "First Name must be more than 2 characters"
        elif postData['first_name'].isalpha() == False:
            errors['first_name'] = "First Name cannot contain numbers"

        if len(postData['last_name']) == 0:
            errors['last_name'] = 'Last Name cannot be empty'
        elif(len(postData['last_name'])) < 2:
            errors['last_name'] = "Last name must be more than 2 characters"
        elif postData['last_name'].isalpha() == False:
            errors['last_name'] = "Last name cannot contain numbers"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address"
        email_validator = User.objects.filter(email=postData['email'])
        if email_validator:
            errors['email'] = "This email already exists."
        if len(email_validator) > 0:
            errors['email'] = "Email already taken"
        if len(postData['email']) == 0:
            errors['email'] = 'Email cannot be empty'
        elif len(postData['email']) < 1:
            errors['email'] = "Email must be more than 2 characters"

        if len(postData['gender']) == 0:
            errors['gender'] = "Gender cannot be empty"
        if len(postData['breed_type']) == 0:
            errors['breed_type'] = "Breed Type cannot be empty"
         
        if len(postData['password']) == 0:
            errors['password'] = "Password cannot be empty"
        elif len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        elif not PASSWORD_REGEX.match(postData['password']):
            errors['password'] = "Password must contain at least one uppercase and one number"

        if len(postData['password_confirmation']) == 0:
            errors['password_confirmation'] = "Confirm Password cannot be empty"
        elif postData['password_confirmation'] != postData['password']:
            errors['password_confirmation'] = "Passwords do not match"
        return errors
    
    def last_validator(self, postData):
        errors = {}
        if len(postData['relationship_goal']) == 0:
            errors['relationship_goal'] = "Relationship goal cannot be empty"
   
        if len(postData['description']) == 0:
            errors['description'] = "Description cannot be empty"
        return errors

    def login_validator(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['input_email']):
            errors['input_email'] = "Unable to log you in"
            return errors

        user = User.objects.filter(email = postData['input_email'])
        print(user)
        if not user:
            errors['input_email'] = "Unable to log you in"
            return errors

        if not bcrypt.checkpw(postData['input_password'].encode(), user[0].password.encode()):
            errors['input_password'] = "Unable to log you in "
            return errors
        return errors

class MessageManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['message']) == 0:
            errors['message'] = "Message cannot be empty"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    gender = models.CharField(max_length= 255)
    breed_type = models.CharField(max_length= 255)
    profile_picture = models.ImageField(upload_to='profile_pictures',blank = True, null=True)
    relationship_goal= models.CharField(max_length = 255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Relationship(models.Model):
    pigOne = models.ForeignKey(User,related_name="liked_by")
    pigTwo = models.ForeignKey(User,related_name="being_liked")
    #0 = pending, 1 = accepted, 2= rejected
    accepted = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Message(models.Model):
    message = models.TextField()
    sender= models.ForeignKey(User, related_name= "sender")
    receiver= models.ForeignKey(User, related_name="receiver")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MessageManager()

