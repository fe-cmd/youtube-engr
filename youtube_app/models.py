from django.db import models
import uuid
from .consts import SORTBY, FEATURES, DURATION, TYPE, UPLOAD_DATE

# Create your models here.
    
class Filters(models.Model):
  sortby = models.CharField(max_length=24, choices=SORTBY)
  features = models.CharField(max_length=24, choices=FEATURES)
  duration = models.CharField(max_length=24, choices=DURATION)
  type = models.CharField(max_length=24, choices=TYPE)
  upload_date = models.CharField(max_length=24, choices=UPLOAD_DATE)

 


    
