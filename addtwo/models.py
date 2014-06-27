from django.db import models

# Create your models here.
class Result(models.Model):
    calculation = models.CharField(max_length="50")
    def __str__(self):
        return self.calculation

        
