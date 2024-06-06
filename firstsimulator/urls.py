from django.urls import path
from . import views

app_name = "firstsimulator"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:controller_id>/contsetting/", views.contsetting, name="contsetting"),
    path("<int:plant_id>/plantsetting/", views.plantsetting, name="plantsetting"),
    path("modelingWithFile/", views.modelingWithFile, name="modelingWithFile"),
    path("pidsimulator/", views.pidSimulatorMain, name="pidsimulator"),
    path("ajax/", views.call_write_data, name="call_write_data"),
]
