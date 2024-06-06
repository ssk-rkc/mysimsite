from django.http import HttpResponse
import csv, os
import pandas as pd
import numpy as np
from . import graph

def process_files(Time_PV, Time_MV):
    Time_PV_dict = convert_to_dict(Time_PV)
    Time_MV_dict = convert_to_dict(Time_MV)
    csv_data = []
    DataLines = list(Time_PV_dict)

    for timeLine in DataLines:
        PV = Time_PV_dict[timeLine]
        MV = Time_MV_dict[timeLine]
        row = [timeLine, PV, MV]
        csv_data.append(row)
    return csv_data

def convert_to_dict(file):
    data = file.read().decode("utf-8")
    lines = data.split("\r\n")
    final_lines = len(lines)-1
    present_lines = 0
    dict = {}
    firstLoop = True

    for line in lines:
        if present_lines < final_lines:
            present_lines +=1
            if firstLoop:
                fields = line.split(",")
                Times = str(fields[0])
                PVorMV = str(fields[1])
                dict[Times] = PVorMV
                firstLoop = False
            else:
                fields = line.split(",")
                Times = fields[0]
                PVorMV = fields[1]
                dict[Times] = PVorMV
        else:
            #Do Nothing
            present_lines = final_lines
    return dict

def write_into_csv(csv_data):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="download.csv"'
    writer = csv.writer(response)
    for row in csv_data:
        writer.writerow(row)

    return response

def save_data_into_csvfile(csv_data, appendname):
    strFile = "./firstsimulator/data/" + appendname + "pid_sim.csv"
    if os.path.isfile(strFile):
        os.remove(strFile)
    else:
        print(strFile)

    with open(strFile, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=",")
        for row in csv_data:
            writer.writerow(row)


def read_csv_for_graph(file):
    df = pd.read_csv(file,index_col=0)
    print(df.head(len(df)))
    print(df.index)
    type(df.index)

def display_graph_with_file(csv_data):
    newfile = split_data(csv_data)
    response = HttpResponse(graph.plotting(newfile), content_type='image/png')

    return response

def display_graph(csv_data, appendname):
    response = HttpResponse(graph.plotting(csv_data, appendname), content_type='image/png')

    return response

def split_data(file):
    data = file.read().decode("utf-8")
    lines = data.split("\r\n")
    final_lines = len(lines)-1
    present_lines = 0
    dict_pv = {}
    dict_mv = {}
    firstLoop = True


    for line in lines:
        if present_lines < final_lines:
            present_lines +=1
            if firstLoop:
                fields = line.split(",")
                Times = str(fields[0])
                PV = str(fields[1])
                MV = str(fields[2])
                dict_pv[Times] = PV
                dict_mv[Times] = MV
                firstLoop = False
            else:
                fields = line.split(",")
                Times = is_float( fields[0] )
                PV = is_float( fields[1] )
                MV = is_float( fields[2] )
                dict_pv[Times] = PV
                dict_mv[Times] = MV
        else:
            #Do Nothing
            present_lines = final_lines

    csv_data = []
    DataLines = list(dict_pv)

    for timeLine in DataLines:
        PV = dict_pv[timeLine]
        MV = dict_mv[timeLine]
        row = [timeLine, PV, MV]
        csv_data.append(row)
    return csv_data


def is_float(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return float(s)
