from django.urls import path

from . import views
from e_blood_bank.views import search_blood

urlpatterns = [
    
    path('login/', views.donor_login, name='donor_login'),
    path('home/', views.home, name='donor_home'),
    path('add_donor/', views.add_donor, name='donor_add'),
    path('search_blood/', search_blood, name='search-blood'),
    # path('update_blood/<int:pk>/', views.update_blood, name='blood_update'),
    # path('delete_blood/<int:pk>/', views.delete_blood, name='blood_delete'),
    # path('requests/' , views.requests, name='bank_requests'),
    # path('requests/update/<int:pk>/', views.update_request, name='update_request'),
    # path('upload', views.upload, name='upload'),
]
