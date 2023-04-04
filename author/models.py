from django.db import models

from authemail.models import  EmailUserManager,EmailAbstractUser

class MyUser(EmailAbstractUser):

    birthday = models.DateField('Dia do nascimento',null=True,blank = True)
    pic_profile = models.ImageField(
        upload_to='profiles/pics/%Y/%m/%d/', blank=True, default='')
    
    objects = EmailUserManager()