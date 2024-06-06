from django.db import models

# Create your models here.


class Controller(models.Model):
    controller_type = models.CharField(max_length=200)
    controller_name = models.CharField("controller name", max_length=200)

    def __str__(self):
        return self.controller_name


class Plant(models.Model):
    plant_type = models.CharField(max_length=200)
    plant_name = models.CharField("plant name", max_length=200)

    def __str__(self):
        return self.plant_name


class contParameter(models.Model):
    controller = models.ForeignKey(Controller, on_delete=models.CASCADE)
    sv = models.IntegerField(default=120)
    const_P = models.IntegerField(default=30)
    const_I = models.IntegerField(default=240)
    const_D = models.IntegerField(default=60)
    do_ARW = models.BooleanField(default=False)
    def __str__(self):
        return self.controller

class plantParameter(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    processGain = models.IntegerField(default=555555)
    timeConst1 = models.IntegerField(default=5555555)
    timeConst2 = models.IntegerField(default=5555555)
    timeConst3 = models.IntegerField(default=5555555)

    def __str__(self):
        return self.plant


class DataForPlot(models.Model):
    TimeForPlot = models.IntegerField()
    PVForPlot = models.IntegerField()
    MVForPlot = models.IntegerField()
