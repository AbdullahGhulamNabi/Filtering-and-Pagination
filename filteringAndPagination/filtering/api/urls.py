from django.urls import path
from .views import  registration_view,RetrieveUpdateDestroyAPIView, BooksAuthorAPIView, BooksAPIView, GenreAPIView
from rest_framework.authtoken.views import obtain_auth_token
from .views import registration_view, logout


urlpatterns = [

    path("register/", registration_view, name="register"),  
    path("AddShowBooks/", BooksAPIView.as_view() , name='all_books'),
    path("AddShowBooks/<int:id>/", BooksAPIView.as_view() , name='each_book'),
    path("AddUpdateBooks/<int:id>/", RetrieveUpdateDestroyAPIView.as_view() , name='each_book'),
    path("genre/", GenreAPIView.as_view() , name='genre'),
    path("Authors/", BooksAuthorAPIView.as_view() , name='authors'),

]