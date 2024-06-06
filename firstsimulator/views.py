from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Controller, contParameter, Plant, plantParameter, DataForPlot
from .functions import process_files
from .functions import write_into_csv, save_data_into_csvfile
from .functions import display_graph
from .functions import split_data
from .forms import ImportDataForm, PidSettingParameterForm, PlantSettingParameterForm, SimSettingParameterForm
from . import pidsimulator, graph, leastSquareMethod
import shutil
import csv


# Create your views here.
def index(request):
    ControllerList = Controller.objects.all()
    PlantList = Plant.objects.all()
    context = {"ControllerList": ControllerList, "PlantList": PlantList,}
    return render(request, "firstsimulator/index.html", context)

def contsetting(request, controller_id):
    controller = get_object_or_404(Controller, pk=controller_id)
    return render(request, "firstsimulator/controllerSetting.html", {"controller": controller})

def plantsetting(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    return render(request, "firstsimulator/plantSetting.html", {"plant": plant})

def call_write_data(request):
    if request.method =='GET':
        pidsimulator.write_csv(request.GET.get("input_data"))
        return HttpResponse()

def modelingWithFile(request):
    coef = [0, 0, 0]

    if request.method == 'POST':
        importdata = ImportDataForm(request.POST, request.FILES)
        if importdata.is_valid():
            Time_PV_MV = request.FILES['Time_PV_MV']
            csv_data = split_data(Time_PV_MV)

            response = graph.plotting(csv_data, appendname="LSM_")
#                display_graph(csv_data, appendname="LSM_"))
            baseData = leastSquareMethod.getDataToMatrix(csv_data)
            data_dt = importdata.cleaned_data['data_Sampling_Time']
            numOfData = importdata.cleaned_data['Number_Of_Data']

            getArraycoefA = leastSquareMethod.calcCoefA(baseData, data_dt, numOfData)
            coef = [ getArraycoefA[0], getArraycoefA[1], getArraycoefA[2] ]
            context = {
                "form": importdata,
                "coef": coef,
                "graph": response
            }


    else:
        importdata = ImportDataForm()
        context = {
            "form": importdata,
            "coef": coef
        }

    return render(request, "firstsimulator/modelingWithFile.html", context)


def modelingWithSeparateDataFile(request):

    if request.method == 'POST':
        importdata = ImportDataForm(request.POST, request.FILES)
        if importdata.is_valid():
            Time_PV = request.FILES['Time_PV']
            Time_MV = request.FILES['Time_MV']

            csv_data = process_files(Time_PV, Time_MV)  #PVとMVがばらばらのファイルを読み込んでTime,PV,MVの並びのデータセットを作る
            response = write_into_csv(csv_data)         #データセットをcsvファイルにして任意の場所に保存する
            graph.plotting(csv_data, appendname="")                    #データセットをグラフ描画する

            return response

    else:
        importdata = ImportDataForm()

    return render(request, "firstsimulator/modelingWithFile.html", {'form':importdata})

def pidSimulatorMain(request):
    if request.method =='GET':
        pidSetting = PidSettingParameterForm(request.session.get('P'))
        plantSetting = PlantSettingParameterForm(request.session.get('coef'))
        simSetting = SimSettingParameterForm(request.session.get('StopTime'))
        context = {
            "pidform": pidSetting,
            "plantform": plantSetting,
            "simform": simSetting
        }
        return render(request, "firstsimulator/pidsimulator.html", context)

    elif request.method == 'POST':
        pidSetting = PidSettingParameterForm(request.POST)
        plantSetting = PlantSettingParameterForm(request.POST)
        simSetting = SimSettingParameterForm(request.POST)

        if pidSetting.is_valid():
            csv_data = pidsimulator.generateControlData(pidSetting.data, plantSetting.data, simSetting.data)
            save_data_into_csvfile(csv_data, appendname='00')
            response = graph.plotting(csv_data, appendname="pid_")
            display_graph(csv_data, appendname="pid_")
            context = {
                "pidform": pidSetting,
                "plantform": plantSetting,
                "simform": simSetting,
                "graph": response
            }


    else:
        pidSetting = PidSettingParameterForm()
        plantSetting = PlantSettingParameterForm()
        simSetting = SimSettingParameterForm()

    context={
        "pidform": pidSetting,
        "plantform": plantSetting,
        "simform": simSetting,
        "graph" : response
    }

    return render(request, "firstsimulator/pidsimulator.html", context)
