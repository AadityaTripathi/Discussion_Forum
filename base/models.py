from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model) :
    name = models.CharField(max_length=200)
    
    def __str__(self) :
        return self.name


class Room(models.Model) : 
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topics = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200) #string with max length 200
    description = models.TextField(null = True, blank = True) 
    # this means that having description is not compusary and can be left blank to be added altter
    #participants =
    updated = models.DateTimeField(auto_now=True) #this takes a snapshort everytime app id updates
    created = models.DateTimeField(auto_now_add=True) # this takes the snpashot only when it is created
    
    class Meta:
        ordering = ['-updated', '-created']
    
    
    def __str__(self) :
        return self.name
    
class Message(models.Model) :
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE) # this means that on deleting room, all the meesages get deleted
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return self.body[0:50]