from typing import Any
from django.shortcuts import render


#Utilities
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

#Models
from .models import Post

from first.models import UserWeb

#Forms
from .forms import PostForm

#Class-view
from django.views.generic import DetailView,ListView,CreateView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin



def search_post(request):
    results = Post.objects.filter(title__startswith=request.GET["post_title"])
    return render(request,template_name="second_templates/looking.html",context={"Posts":results,"Searched":request.GET["post_title"]})

class UserDetailView(LoginRequiredMixin,DetailView):
    
    model = UserWeb
        
    template_name= "second_templates/details.html"
    
    slug_field = "pk"#El tipo de dato que tomaremos del modelo queryset
    
    slug_url_kwarg = "pk"#Es el nombre que esta en la url
    
    context_object_name = "user"#El nombre del objecto que estamos pasando(Por defecto tendra el mismo nombre del modelo)
    
    queryset = UserWeb.objects.all()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add user's posts to context"""
        
        context = super().get_context_data(**kwargs)#Regresa el diccionario que contiene el modelo
        
        user = self.get_object()#Regresa el objeto que esta en el queryset
        
        context["posts"] = Post.objects.filter(from_user=user).order_by("-created")#Se le agrega al diccionario los posts que pertenecen a cada user y los ordena
        
        return context #regresa el diccionario




class PostListView(LoginRequiredMixin,ListView):
    
    model = Post#Modelo por el cual se listaran los datos
    
    template_name = "second_templates/Posts.html"#El template a mostrar
    
    paginate_by = 20#Se establece la cantidad de  objeto que se daran, o paginacion
    
    context_object_name = "Posts"#Nombre del objeto



class DetailPostView(LoginRequiredMixin,DetailView):
    
    model = Post#Usa el modelo por el que se listaran sus objetos
    template_name = "second_templates/list_post.html"#Se establece el template a renderizar
    context_object_name = "Post"#Se le coloca el nombre de los objetos a pasar como contexto
    queryset = Post.objects.all()#Se le pasa la lista de objetos a mostrar
    slug_field = "pk"#la propiedad que vamos a utilizar en el modelo
    slug_url_kwarg = "pk"#El nombre de la propiedad pasada como parametro, que se refleja en la url.py



class CreatePostView(LoginRequiredMixin,CreateView):
    
    model = Post#Se le pasa el modelo por el que se creara un objeto
    
    template_name = "second_templates/create_post.html"#Nombre del template
    
    success_url = reverse_lazy("GETTINGPOSTS")#Este pide que se le de una url de manera reversiva, pero solo cuando la necesite
    
    context_object_name = "form"#El nombre por el cual se hara referencia al formulario
    
    form_class = PostForm#Aqui usa el modelo para crear el objeto(Se pueden hacer tanto model o form)
    #En este caso toma como prioridad el form,
    
    
    #Explicar ocmo funciona
    
    def form_valid(self, form):
        form.instance.from_user = self.request.user#Toma instancia del formulario
        #Este usa el campo from_user y dice que va a ser igual a el usuario autenticado
        
      
        return super().form_valid(form)#Luego se valida nuevamente con el formulario modificado
    
    
    
    
    
    
    
    
    
# @login_required
# def getting_posts(request):
    
#     posts = Post.objects.all()
    
#     return render(request,template_name="second_templates/Posts.html",context={"Posts":posts})


    
    
    
    
    
    
# @login_required
# def share_post(request):
#     if request.method == "GET":
        
#         return render(request,template_name="second_templates/create_post.html",context={"form":PostForm})
    
#     else:
        
#         form = PostForm(data=request.POST,files=request.FILES,instance=Post(from_user=request.user))
        
#         if form.is_valid():
           
#             form.save()
            
#             messages.success(request,"Tu post se ha publicado")
#             return redirect("GETTINGPOSTS")
        
#         else:
#             messages.error(request,f"{form.errors}")
#             return redirect("SHARE_POST")
        


#from django.http import JsonResponse

# #Geolocation
# from django.contrib.gis.geoip2 import GeoIP2
# # Create your views here.

# g = GeoIP2()

# print(g.city("80.8.41.38"))
