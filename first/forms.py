from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


#Modelos
from .models import UserWeb

""" Estoy creando los formularios para poder hashear la contraseña debido a que al usar AbstracUser
    estoy quitandole una serie de procedimientos que realiza mediante formularios y otros
    ---Aqui solo estoy creando formularios que heredan de el modelo userweb-que a su vez este hereda de
    AbstractUser"""


"""Donde estos formularios heredan de los formularios de change y create de auth"""

#class CustomUserChangeForm(UserChangeForm):
   # pass

# class CustomUserUpdateForm(CustomUserChangeForm):
#     password = None
    
#     profile_picture = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control"}))
    
#     biography = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","required":"True"}))
    
#     phone_number = forms.CharField(widget=forms.NumberInput(attrs={"class":"form-control","required":"True"}))

    
#     # class Meta:
#     #     model = UserWeb
#     #     fields = ["profile_picture","biography","phone_number"]
#     #     widgets = {
#     #         "profile_picture":forms.FileInput(attrs={"class":"form-control"}),
#     #         "biography":forms.Textarea(attrs={"class":"form-control","required":"True"}),
#     #         "phone_number":forms.NumberInput(attrs={"class":"form-control","required":"True"})
#     #     }


class CustomUserUpdateForm(forms.Form):
    
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control"}))
    
    biography = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","required":"True"}),max_length=500)
    
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={"class":"form-control","required":"True"}),max_length=15)



class CustomUserCreationForm(forms.Form):
    profile_picture = forms.ImageField(widget=forms.FileInput(
                attrs={"class":"form-control",
                       "style" : "",
                       "type":"file",
                       "placeholder":"Foto de perfil",
                       "id":"image_field_id",
                       "style":"border-color: black;"}))
    
    username = forms.CharField(
        min_length=4,
        max_length=50,
        label=False,
        widget=forms.TextInput(
                attrs={"class":"form-control",
                       "style":"border-color: black;",
                       "placeholder":"Nombre de usuario"}))
  
    
    first_name = forms.CharField(
        min_length=2,
        max_length=50,
        label=False,
        widget=forms.TextInput(
                attrs={"class":"form-control",
                       "placeholder":"Nombre",
                       "style":"border-color: black;",
                       "label":"Nombre",
                       "required":"True"}))
    
  
    
    last_name = forms.CharField(
        min_length=2,
        max_length=50,
        label=False,
        widget=forms.TextInput(
            attrs={"class":"form-control","placeholder":"Apellido","required":"True","style":"border-color: black;"}))
    
    email = forms.CharField(
        max_length=254,
        label=False,
        widget=forms.EmailInput(
            attrs={"class":"form-control","placeholder":"Correo electronico","required":"True","style":"border-color: black;"}))
    
    
    password1 = forms.CharField(
        max_length=70,
        label=False,
        strip=False,
        widget=forms.PasswordInput(
        attrs={"autocomplete": "new-password",
               "class":"form-control",
               "style":"border-color: black;",
               "placeholder":"Contraseña"}))
    
    password2 =  forms.CharField(
        max_length=70,
        label=False,
        strip=False,
        widget=forms.PasswordInput(
        attrs={"autocomplete": "new-password",
               "class":"form-control",
               "style":"border-color: black;",
               "placeholder":"Confirma tu contraseña"}))
    
        

        #clean lo que hace es devolver los datos limpios
        #SIEMPRE RETORNAR LOS DATOS QUE SE USAN
        
        #Aqui sobreescribimos el metodo clean
    def clean_username(self):
        username = self.cleaned_data["username"]
        query = UserWeb.objects.filter(username=username).exists()
            
        if query:
            raise forms.ValidationError("Usuario ya existe en la base de datos")
            
        return username

        #Aqui usamos el metodo antes de que fuera sobreescrito con heradacion de super
       
    def clean_password2(self):
        password = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return password




# class CustomUserCreationForm(UserCreationForm):
    
#     profile_picture = forms.ImageField(widget=forms.FileInput(
#                 attrs={"class":"form-control",
#                        "style" : "",
#                        "type":"file",
#                        "placeholder":"Foto de perfil",
#                        "id":"image_field_id",
#                        "style":"border-color: black;"}))
    
#     username = forms.CharField(
#         min_length=4,
#         max_length=50,
#         label=False,
#         widget=forms.TextInput(
#                 attrs={"class":"form-control",
#                        "style":"border-color: black;",
#                        "placeholder":"Nombre de usuario"}))
    
#     password1 = forms.CharField(
#         max_length=70,
#         label=False,
#         strip=False,
#         widget=forms.PasswordInput(
#         attrs={"autocomplete": "new-password",
#                "class":"form-control",
#                "style":"border-color: black;",
#                "placeholder":"Contraseña"}))
    
#     password2 =  forms.CharField(
#         max_length=70,
#         label=False,
#         strip=False,
#         widget=forms.PasswordInput(
#         attrs={"autocomplete": "new-password",
#                "class":"form-control",
#                "style":"border-color: black;",
#                "placeholder":"Confirma tu contraseña"}))
    
  
    
#     first_name = forms.CharField(
#         min_length=2,
#         max_length=50,
#         label=False,
#         widget=forms.TextInput(
#                 attrs={"class":"form-control",
#                        "placeholder":"Nombre",
#                        "style":"border-color: black;",
#                        "label":"Nombre",
#                        "required":"True"}))
    
  
    
#     last_name = forms.CharField(
#         min_length=2,
#         max_length=50,
#         label=False,
#         widget=forms.TextInput(
#             attrs={"class":"form-control","placeholder":"Apellido","required":"True","style":"border-color: black;"}))
    
#     email = forms.CharField(
#         max_length=254,
#         label=False,
#         widget=forms.EmailInput(
#             attrs={"class":"form-control","placeholder":"Correo electronico","required":"True","style":"border-color: black;"}))
        

#         #clean lo que hace es devolver los datos limpios
#         #SIEMPRE RETORNAR LOS DATOS QUE SE USAN
        
#         #Aqui sobreescribimos el metodo clean
#     def clean_username(self):
#         username = self.cleaned_data["username"]
#         query = UserWeb.objects.filter(username=username).exists()
            
#         if query:
#             raise forms.ValidationError("Usuario ya existe en la base de datos")
            
#         return username

#         #Aqui usamos el metodo antes de que fuera sobreescrito con heradacion de super
       
#     def clean_password2(self):
#         password = self.cleaned_data["password1"]
#         password2 = self.cleaned_data["password2"]

#         if password != password2:
#             raise forms.ValidationError("Las contraseñas no coinciden")

#         return password

            





# class SignupForm(forms.Form):
#     """Sign up form."""

#     username = forms.CharField(min_length=4, max_length=50)

#     password = forms.CharField(
#         max_length=70,
#         widget=forms.PasswordInput()
#     )
#     password_confirmation = forms.CharField(
#         max_length=70,
#         widget=forms.PasswordInput()
#     )

#     first_name = forms.CharField(min_length=2, max_length=50)
#     last_name = forms.CharField(min_length=2, max_length=50)

#     email = forms.CharField(
#         min_length=6,
#         max_length=70,
#         widget=forms.EmailInput()
#     )

#     def clean_username(self):
#         """Username must be unique."""
#         username = self.cleaned_data['username']
#         username_taken = User.objects.filter(username=username).exists()
#         if username_taken:
#             raise forms.ValidationError('Username is already in use.')
#         return username

#     def clean(self):
#         """Verify password confirmation match."""
#         data = super().clean()

#         password = data['password']
#         password_confirmation = data['password_confirmation']

#         if password != password_confirmation:
#             raise forms.ValidationError('Passwords do not match.')

#         return data

#     def save(self):
#         """Create user and profile."""
#         data = self.cleaned_data
#         data.pop('password_confirmation')

#         user = User.objects.create_user(**data)
#         profile = Profile(user=user)
#         profile.save()


# class ProfileForm(forms.Form):
#     """Profile form."""

#     website = forms.URLField(max_length=200, required=True)
#     biography = forms.CharField(max_length=500, required=False)
#     phone_number = forms.CharField(max_length=20, required=False)
#     picture = forms.ImageField()