from django.contrib import admin



#Modelo Usuario
from .models import UserWeb


#Modelo UserAdmin
from django.contrib.auth.admin import UserAdmin

#Formularios
from .forms import CustomUserCreationForm,CustomUserUpdateForm

# Register your models here.


#admin.site.register(UserWeb)

#FALTO AÑADIR PARA ENCRIPTAR LA CONTRASEÑA

#Aqui tengo que crear otro usuario admin que le da parametros de creacion y cambio mediante los formularios
#creados en forms.py que añaden seguridad a ciertos campos como es la contraseña
#le doy la posibilidad de cambiar con CustomUserChangeForm y la de crear con UserCreationForm
#La diferencia con este y los demas, es que este tiene password hasheada y mas
#Y le añado al custom user admin los campos que se encuentran en userADMIN

class CustomUserAdmin(UserAdmin):
    form = CustomUserUpdateForm
    add_form = CustomUserCreationForm
    fieldsets = UserAdmin.fieldsets 
    #AÑADIENDO CAMPOS A LA CREACION DE
    add_fieldsets = (
        (
            "Userweb",{
                "fields":(("username","profile_picture",),
                          ("password1","password2")
                          ),
            }
            
        ),
        (
            "Extra_information",{
                "fields":(("phone_number","email","website"),
                          ("biography"),)
            }),
        (
            "Metadata",{
                "fields":((
                    "created","modified",
                ))
            }
        )
    )
    


#Luego que se le da el acceso a crear y modificar usuarios mediante los change y creation forms
#Se registra en el panel de admin
#Pero haciendo que herede de este mismo de CustomUserAdmin

class UserWebAdmin(CustomUserAdmin):
    """Modifying display on django site"""
    
    
    #Se muestra en el panel cada campo
    list_display = ["pk","username","phone_number","email","website","profile_picture"]
    
    #Se coloca un link por cada campo que dirije al usuario
    list_display_links = ["pk","username"]
    
    #Se le da la posibilidad de editar campos sin entrar al perfil
    list_editable = ["phone_number","email","website"]
    
    #Se buscara por los siguientes campos
    search_fields = ["username","email","phone_number","pk"]
    
    #Se hace una lista de filtros para la busqueda de estos
    list_filter = ["created","modified","is_staff"]
    
    
    #Se incluye lo que se mostrara al solicitar los datos en el usuario para editarlo
    fieldsets = (
        (
            "Userweb",{
                "fields":(("username","profile_picture",),
                          ("password")
                          ),
            }
            
        ),
        (
            "Extra_information",{
                "fields":(("phone_number","email","website"),
                          ("biography"),
                          ("first_name","last_name"))
            }),
        (
            "Metadata",{
                "fields":((
                    "created","modified",
                ))
            }
        ),
        (
            "Admindata",{
                "fields":((
                    "is_active","is_staff","is_superuser"
                ),(
                    "date_joined","last_login"
                ))
            }
        ),
        
        
    )
    
    readonly_fields = ["created","modified"]
    
    




admin.site.register(UserWeb)

#Al crear un usuario se podran colocar todos los datos en un solo template solo funciona con llaves foraneas
# class UserWebInline(admin.StackedInline):
    
#     model = UserWeb
#     can_delete = False
#     verbose_name_plural = "UsersWeb"


# class UserAdmin(UserAdmin):
#     inlines = (UserWebInline,)

