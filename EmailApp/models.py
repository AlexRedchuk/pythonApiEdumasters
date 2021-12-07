from django.db import models

# Create your models here.

class EmailInfo(models.Model) :
    EmailInfoId = models.AutoField(primary_key=True)
    EmailInfoUserEmail = models.CharField(max_length=500, unique=True)
