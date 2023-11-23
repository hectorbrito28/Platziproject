from django.db import models

from django.conf import settings

# Create your models here.


class Post(models.Model):
    
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    postimg  = models.ImageField(upload_to="post_images/")
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created"]
    
    
    def __str__(self) -> str:
        return f"{self.title} ----- {self.from_user}"