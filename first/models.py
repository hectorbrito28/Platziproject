from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserWeb(AbstractUser):
    
    profile_picture = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        default="static_images/user.png")#Subo la imagen a la ruta de MEDIA_URL
    
    website = models.URLField(max_length=254,blank=True,null=False)
    biography = models.TextField(max_length=500,blank=True,null=False)
    phone_number = models.CharField(max_length=15,blank=True,null=False)
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    



#Usar OneToOnefield es una buena opcion para heredar los datos de user de django.

#Abstractuser solo modifica directamente el modelo