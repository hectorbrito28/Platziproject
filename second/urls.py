from django.urls import path
from . import views as v2


from .views import UserDetailView




urlpatterns = [
    path("search_posts/",v2.search_post,name="Search"),
    path("Posts/",v2.PostListView.as_view(),name="GETTINGPOSTS"),
    path("new_posting/",v2.CreatePostView.as_view(),name="SHARE_POST"),
    path("profile/details/<int:pk>",UserDetailView.as_view(),name="DETAILS"),
    path("Posts/details/<int:pk>",v2.DetailPostView.as_view(),name="DETAILSPOST")
]