from django.contrib import admin
from .models import Post
# Register your models here.



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["pk","from_user","title","created","postimg"]
    
    list_editable = ["title","postimg"]
    
    list_display_links = ["pk","from_user"]