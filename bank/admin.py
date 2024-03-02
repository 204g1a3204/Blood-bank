from django.contrib import admin
from bank.models import BloodBank , Blood, State, City


admin.site.register(State)
admin.site.register(City)

admin.site.register(BloodBank)
admin.site.register(Blood)

