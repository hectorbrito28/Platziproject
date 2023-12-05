#Django
from django.shortcuts import redirect

#Utilities
from django.urls import reverse_lazy,reverse
import requests
import secrets
from django.contrib.auth.hashers import check_password
#Models
from second.models import Post
from .models import UserWeb

#forms
from .forms import CustomUserCreationForm,CustomUserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin

#Class-based views
from django.views.generic import FormView
from django.contrib.auth.views import LoginView ,LogoutView

#DATABASE FIREBASE STORAGE

import pyrebase




config = {
    "apiKey": "AIzaSyCPnGOBb3-RNLw8XFeUzGfjYvb9yuaOhS4",
    "authDomain": "platzi-gram-af3b9.firebaseapp.com",
    "projectId": "platzi-gram-af3b9",
    "storageBucket": "platzi-gram-af3b9.appspot.com",
    "messagingSenderId": "175087990376",
    "appId": "1:175087990376:web:e16fa92cd47877f38e6ddd",
    "measurementId": "G-58ELGL2XGD",
    "databaseURL" : "",
    "serviceAccount":"admin_platzigram.json"
}


firebase = pyrebase.initialize_app(config)

storage = firebase.storage()

auth = firebase.auth() 


class SignupFormView(FormView):
    
    
    template_name = "first_templates/signup.html"
    
    form_class = CustomUserCreationForm
    
    success_url = reverse_lazy("Signin")
    
    context_object_name ="form"
    
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("GETTINGPOSTS")
        return super().get(request, *args, **kwargs)
    
    
    def form_valid(self, form):
        
        #Obteniendo contraseña verificada
        password1 = form.clean_password2()
        
        #Obteniendo email
        email = form.cleaned_data["email"]
        
        #Obteniendo imagen
        profile_picture = form.cleaned_data["profile_picture"]
        
        
        #Creando cuenta en firebase storage
        try:
            user = auth.create_user_with_email_and_password(email,password1)
        except:
             return self.render_to_response(self.get_context_data(form=form, error= "Email ya existe en la base de datos"))
            

        #Iniciando sesion en cuenta temporalmente para guardar la imagen de usuario
        account_created = auth.sign_in_with_email_and_password(email,password1)
        
        user_id = account_created["localId"]
        
        image_exist = storage.child(f"{user_id}/images/user_images/" + profile_picture.name).get_url(None)
        
        response  = requests.get(image_exist)
        
        
        if response.status_code == 200:
            image_id = str(secrets.token_hex(16))
            
            #saving image into firebase storage
            storage.child(f"{user_id}/images/user_images/" + profile_picture.name + "__" + image_id).put(profile_picture.read(),content_type=profile_picture.content_type)
            
            #Get image_url from firebase storage
            image_url = storage.child(f"{user_id}/images/user_images/" + profile_picture.name + "__" + image_id).get_url(None)
            
            #Creating an object task with image_url link 
            UserWeb.objects.create_user(
            profile_picture = image_url,
            first_name = form.cleaned_data["first_name"],
            last_name = form.cleaned_data["last_name"],
            username = form.cleaned_data["username"],
            email = email,
            password =password1,
            )
            
            
        
        else:
            
            #saving image into firebase storage
            storage.child(f"{user_id}/images/user_images/" + profile_picture.name).put(profile_picture.read(),content_type=profile_picture.content_type)
            
            #Get image_url from firebase storage
            image_url = storage.child(f"{user_id}/images/user_images/" + profile_picture.name).get_url(None)
            
            #Creating an object task with image_url link 
            UserWeb.objects.create_user(
            profile_picture = image_url,
            first_name = form.cleaned_data["first_name"],
            last_name = form.cleaned_data["last_name"],
            username = form.cleaned_data["username"],
            email = email,
            password =password1,
            )
            
        
        
        
        
        
        
        #form.save()#Guarda el formulario, es mejor usar createview que formview para crear objetos
        return super().form_valid(form)




class LoginUserView(LoginView):
    
    
    template_name = "first_templates/signin.html"
    
    redirect_field_name = reverse_lazy("GETTINGPOSTS")
    
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        
        
        user = UserWeb.objects.filter(username=form.cleaned_data["username"])
        
        user = user[0]
        
        email = user.email
        
        password_encoded = user.password
        
        password_form = form.cleaned_data["password"]
        
        if check_password(password_form,password_encoded):
            
            
            firebase_user = auth.sign_in_with_email_and_password(email,password_form)
        
        
            #Coloca la session de auth-firebase en session del request
            self.request.session["user_firebase"] = firebase_user
            
            print("Sesion iniciada")
            
           

        
        
        return super().form_valid(form)



class LogoutUserView(LogoutView):
    
    template_name = "first_templates/signin.html"

   
class UpdateUserView(LoginRequiredMixin,FormView):
    
    model = UserWeb
    template_name = "first_templates/update_account.html"
    #fields = ["biography","profile_picture","phone_number"]
    form_class = CustomUserUpdateForm
    
    
    def get_initial(self):
        form_values = {
            "biography":self.request.user.biography,
            "phone_number":self.request.user.phone_number,
        }
        return form_values

    
    def get_object(self):
        return self.request.user
    
    def get_success_url(self):
        pk = self.request.user.pk
        return reverse("DETAILS",kwargs={"pk":pk})

    def form_valid(self, form) :
        
        
        image = form.cleaned_data["profile_picture"]
        
        user_id = self.request.session["user_firebase"]["localId"]
        
        image_exist = storage.child(f"{user_id}/images/user_images/" + image.name).get_url(None)
        
        response  = requests.get(image_exist)
        
        
        if response.status_code == 200:
            image_id = str(secrets.token_hex(16))
            
            #saving image into firebase storage
            storage.child(f"{user_id}/images/user_images/" + image.name + "__" + image_id).put(image.read(),content_type=image.content_type)
            
            #Get image_url from firebase storage
            image_url = storage.child(f"{user_id}/images/user_images/" + image.name + "__" + image_id).get_url(None)
            
            #Updating self-user with image_url link 
            
            user = UserWeb.objects.get(id=self.request.user.id)
            
            user.profile_picture = image_url
            
            user.biography = form.cleaned_data["biography"]
            
            user.phone_number = form.cleaned_data["phone_number"]
        
            user.save()
            
        
        else:
            
            #saving image into firebase storage
            storage.child(f"{user_id}/images/user_images/" + image.name).put(image.read(),content_type=image.content_type)
            
            #Get image_url from firebase storage
            image_url = storage.child(f"{user_id}/images/user_images/" + image.name).get_url(None)
            
            #Updating self-user with image_url link 
            user = UserWeb.objects.get(id=self.request.user.id)
            
            user.profile_picture = image_url
            
            user.biography = form.cleaned_data["biography"]
            
            user.phone_number = form.cleaned_data["phone_number"]
            
            user.save()
        
        return super().form_valid(form)









# #forms
# from .forms import CustomUserCreationForm,CustomUserChangeForm,CustomUserUpdateForm
# from django.contrib.auth.forms import AuthenticationForm


#from django.http import HttpResponse,HttpResponseRedirect

#Utilities
#from datetime import datetime
#from django.contrib import messages
#from django.contrib.auth.hashers import check_password
#from django.contrib.auth import authenticate,login,logout
#from django.utils.datastructures import MultiValueDict
#from django.contrib.auth.decorators import login_required

# from typing import Any
# from django.db import models

# def signupview(request):
#     if request.method == "GET":
#         return render(request,template_name="first_templates/signup.html",context={"form":CustomUserCreationForm})
#     else:

        
#         form = CustomUserCreationForm(request.POST,request.FILES)

#         if form.is_valid():
#             form.save()
#             messages.success(request,"Tu cuenta se ha creado exitosamente")
#             return redirect("Signin")
#         else:
#             messages.error(request,f"{form.errors}")
       
            
#         return redirect("Signup")


# def signinview(request):
#     if request.method == "GET":
#         return render(request,template_name="first_templates/signin.html",context={"form":CustomUserCreationForm})
    
#     else:

        
#         form = AuthenticationForm(data={"username":request.POST["username"],"password":request.POST["password1"]})  
#         if form.is_valid():
            
#             username = form.cleaned_data.get("username")
            
#             password = form.cleaned_data.get("password")
            
#             user = UserWeb.objects.get(username=username)
            
#             if check_password(password,user.password):
                
#                 auth = authenticate(request,username=username,password=password)
                
#                 login(request,auth)
                
#                 messages.success(request,"Iniciado sesion correctamente")
                
#                 return redirect("GETTINGPOSTS")

            
#             else:
#                 messages.error(request,f"{form.errors}")
        
#         else:
#             messages.error(request,f"{form.errors}")
        
#         return redirect("Signin")
                
                
# 


#def logoutview(request):
#     logout(request)
#     messages.success(request,"Se ha cerrado la sesion")
#     return redirect("Signin")



# @login_required
# def update_account(request):
#     if request.method == "GET":
        
#         user = request.user
        
#         return render(request,template_name="first_templates/update_account.html",context={"form":CustomUserUpdateForm,"user":user})

#     else:
        
#         user = UserWeb.objects.get(id=request.user.id)
        
#         user.biography = request.POST["biography"]
        
#         file  =  request.FILES.get("profile_picture",None)
        
#         if file:
#             user.profile_picture.delete()
#             user.profile_picture = request.FILES.get("profile_picture")
        
            
#         user.phone_number = request.POST["phone_number"]
        
#         user.save()
        
#         return redirect("DETAILS",request.user.id)











































































   # content = []
    # for i in u:
    #     content.append(
    #         """<p><strong>{name}</strong></p>
    #             <p><small>{time}</small></p>
    #             <figure><img src="{picture}" style="width:100px; heigth:100px;"></figure>""".format(**i)
    #     )







# u = [
#     {   
        
#         "name":"Juan",
#         "user":{"Profile_picture":"https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1","username":"Juanpa"},
#         "time":datetime.now().strftime("%b %dth, %Y - %H:%M hrs "),
#         "picture":"https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg"
#     },
#     {
#         "name":"Maria",
#         "user":{"Profile_picture":"https://img.freepik.com/fotos-premium/dominante-juego-sexual-preliminar-dominar-obedecer-desvestirse-seducir-companero-brutal-hombre-guapo_265223-48356.jpg?w=360","username":"Mary"},
#         "time":datetime.now().strftime("%b %dth, %Y - %H:%M hrs "),
#         "picture":"https://img.freepik.com/fotos-premium/chica-joven-quiere-desnudarse_391052-8706.jpg?w=1060"
#     },
#     {
#         "name":"Alz",
#         "user":{"Profile_picture":"https://img.freepik.com/fotos-premium/labios-mujer-chupando-caramelo-mujer-desnuda-juguetona-labios-color-rosa-brillante-piruleta-boca-l_265223-62076.jpg?w=1060","username":"alz23"},
#         "time":datetime.now().strftime("%b %dth, %Y - %H:%M hrs "),
#         "picture":"https://img.freepik.com/foto-gratis/puente-madera-isla-koh-nangyuan-surat-thani-tailandia_335224-1082.jpg?w=1060&t=st=1699452058~exp=1699452658~hmac=abd2f6c45318a338d2f08948b5eaf6285f32dabccfd365727d40c253c3882b4a"
#     }
# ]
