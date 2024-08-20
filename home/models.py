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
    

    #owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.contact

    class Meta:
        ordering: ['-date_ordered']




class Status(models.Model):
     name =  models.CharField(max_length=30)    



class Profile(models.Model):
    name = models.CharField(max_length=100)
    email = models.TextField() 
    password = models.TextField()  
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)      




class Payment(models.Model):
     name =  models.CharField(max_length=30)   

