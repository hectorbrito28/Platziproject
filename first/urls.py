"""First urls.py file"""

from django.urls import path
from . import views as v
from django.views.generic import TemplateView


urlpatterns = [
    path("",TemplateView.as_view(template_name="first_templates/Home.html")),
    path("Signup/",v.SignupFormView.as_view(),name="Signup"),
    path("Signin/",v.LoginUserView.as_view(),name="Signin"),
    path("logout/",v.LogoutView.as_view(),name="Logoutview"),
    path("update/",v.UpdateUserView.as_view(),name="Update"),
    
    
]

