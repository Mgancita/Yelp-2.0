from django.db import models

# Create your models here.    

class Resturant(models.Model):
    # Resturant name
    name = models.CharField(max_length=255, null=False)
    # name of location
    location = models.CharField(max_length=255, null=False)
    #contact 
    contact = models.CharField(max_length=20,null=False)
    #rating
    rating = models.FloatField(default=0.0)
    
    

    def __str__(self):
        return "{} - {} - {} - {}".format(self.name, self.location,self.contact,self.rating)