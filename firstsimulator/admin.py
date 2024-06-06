from django.contrib import admin
from .models import Controller, contParameter, Plant, plantParameter, DataForPlot

# Register your models here.
admin.site.register(Controller)
admin.site.register(contParameter)
admin.site.register(Plant)
admin.site.register(plantParameter)
admin.site.register(DataForPlot)
