from django.urls import path
from . import views
from e_blood_bank.views import search_blood

urlpatterns = [
    path('login/', views.hospital_login, name='hospital_login'),
    path('home/', views.home, name='hospital_home'),
    path('add_hospital/', views.add_hospital, name='add_hospital'),
    path('add_bed/', views.add_bed, name='add_bed'),
    path('requests/' , views.requests, name='requests'),
    path('requests/delete/<int:pk>/', views.delete_request, name='delete_request'),
    path('raise_request/', views.raise_request, name='raise_request'),
    path('update_bed/<int:pk>/', views.update_bed, name='update_bed'),
    path('delete_bed/<int:pk>/', views.delete_bed, name='delete_bed'),
    path('search_blood/', search_blood, name='search-blood'),
]
