from django.urls import path

from . import views
from e_blood_bank.views import search_blood

urlpatterns = [
    
    path('login/', views.bank_login, name='bank_login'),
    path('home/', views.home, name='bank_home'),
    path('add_bank/', views.add_bank, name='bank_add'),
    path('add_blood/', views.add_blood, name='blood_add'),
    path('update_blood/<int:pk>/', views.update_blood, name='blood_update'),
    path('delete_blood/<int:pk>/', views.delete_blood, name='blood_delete'),
    path('requests/' , views.requests, name='bank_requests'),
    path('requests/update/<int:pk>/', views.update_request, name='update_request'),
    path('upload', views.upload, name='upload'),
    path('get_cities/<int:state_id>/', views.get_cities, name='get_cities'),
    path('search_blood/', search_blood, name='search-blood'),
]
