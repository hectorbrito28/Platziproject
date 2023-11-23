from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    title = forms.CharField(
        label="Titulo",
        max_length=250,
        widget=forms.TextInput(attrs={"class":"form-control"}))
    
    description = forms.CharField(
        label="Descripcion",
        widget=forms.Textarea(attrs={"class":"form-control"}))
    
    postimg = forms.ImageField(
        label="Imagen",
        widget=forms.FileInput(
            attrs={"class":"form-control"}))

    class Meta:
        model = Post
        fields = ["title","description","postimg"]