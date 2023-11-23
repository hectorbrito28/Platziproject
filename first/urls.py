"""First urls.py file"""

from django.urls import path
from . import views as v



urlpatterns = [
    path("Signup/",v.SignupFormView.as_view(),name="Signup"),
    path("Signin/",v.LoginUserView.as_view(),name="Signin"),
    path("logout/",v.LogoutView.as_view(),name="Logoutview"),
    path("update/",v.UpdateUserView.as_view(),name="Update"),
    
    
]

