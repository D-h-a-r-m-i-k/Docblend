from django.contrib import admin
from django.db import models



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    
class Task(models.Model):
    description = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.description
    
admin.site.register(ContactMessage)
admin.site.register(Task)

