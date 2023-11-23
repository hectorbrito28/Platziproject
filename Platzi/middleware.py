"""MIDDLEWARES.PY"""

#Django 

from django.shortcuts import redirect

#Utilities
from django.urls import reverse
from django.contrib import messages
from django.conf import settings


#Explicar como y cuando se ejecutan los middleware


# request.path.startswith('/profile_images/') evitando que se meta en admin

#Los middlewares se ejecutan antes y despues de una peticion
#Este por ejemplo se esta ejecutando luego de que el usuario se autentique
#Reverse funciona de manera que te devuelve por asi decirlo por el mismo camino por donde entraste
#redirect da la vuelte por asi decirlo



""" En esa funcion request.user.is_anonymous es aquel usuario anonimo que no esta autenticado"""

""" si no es staff seguira, y si el usuario no tiene biografia o numero de telefono lo va a redireccionar a  update"""

""" Pero si la direccion del request es alguna de las que estan ahi como Logout o cualquier direccion que comience por profile_images"""

"""No la enviara a update"""

"""Por ultimo el response sera igual a get_response con parametro request"""

def completeaccount_middleware(get_response):
    
    
    def middleware(request):
        
        
        
        if not request.user.is_anonymous:
            print("goasfa")
                
            if not request.user.is_staff:
                    
                if not request.user.biography or not request.user.phone_number:
                   
                    if request.path not in [reverse("Update"),reverse("Logoutview")] and not request.path.startswith("/static/") and not request.path.startswith("/admin/"):
                        messages.success(request,"Necesitas completar tu cuenta antes de ingresar correctamente")
                        return redirect("Update")   
        
        response = get_response(request)
        return response
    
    return middleware