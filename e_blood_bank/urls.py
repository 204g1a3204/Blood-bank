from django.contrib import admin
from django.urls import path, include

from bank import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("upload/",views.upload,name="upload"),
    path("", views.index, name="home"),
    path('logout/' , views.logout, name="logout"),
    path("bank/", include("bank.urls")),
    path("hospital/", include("hospital.urls")),
    path("donor/", include("donor.urls")),
]
