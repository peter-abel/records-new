from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


# Create your models here.
class NewOrder(models.Model):
    name = models.CharField(max_length=100)
    contact = models.TextField()
    location = models.TextField()
    quantity = models.IntegerField()
    date_ordered = models.DateField(default=now)
    date_due = models.DateField()
    status = models.CharField(max_length=30)
    pay_form = models.CharField(max_length=30)
    amount = models.IntegerField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, blank=True)
    

    def __str__(self):
        return f"{self.name} - {self.contact}"

    class Meta:
        ordering: ['-date_ordered']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=100) 

    def __str__(self):
        return self.user.username




class Status(models.Model):
     name =  models.CharField(max_length=30)    



    




class Payment(models.Model):
     name =  models.CharField(max_length=30)   

