from django.contrib import admin

from .models import *

admin.site.register(Hospital)
admin.site.register(BloodRequest)
admin.site.register(Bed)