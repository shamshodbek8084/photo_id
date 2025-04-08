from django.db import models

# Create your models here.

class Citizen(models.Model):
    name = models.CharField(max_length=256)
    bio = models.TextField()
    image = models.ImageField(upload_to='images/')


    def __str__(self):
        return self.name
    