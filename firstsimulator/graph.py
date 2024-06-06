import base64
import os
import io
import matplotlib
import numpy as np

matplotlib.use("Agg")
from matplotlib import pyplot as plt

def PlotGraphWithCsv(csv_data):
    firstLoop = True
    for data in csv_data:
        if firstLoop:
            firstLoop = False
        else:
            plt.plot(data[0],data[1])

    plt.figure(figsize=(10,5))
    plt.xticks(rotation=45)
    plt.title("PV trend ℃")
    plt.xlabel("TimeForPlot")
    plt.ylabel("PVForPlot")
    plt.tight_layout()
    plt.show()
    return True

def plotting(csvdata, appendname):
    firstLoop = True
    final_lines = len(csvdata)-2
    present_lines = 0
    xmin = 0
    ymin = 0
    xmax = 600
    ymax = 150

    xlist = []
    pvlist = []
    mvlist = []
    for data in csvdata:
        if present_lines < final_lines:
            present_lines +=1
            if firstLoop:
                firstLoop = False
            elif present_lines < 2:
                xlist.append(data[0])
                pvlist.append(data[1])
                mvlist.append(data[2])
                xmin = float(data[0])
                ymin = float(data[1])
            else:
                xlist.append(data[0])
                pvlist.append(data[1])
                mvlist.append(data[2])
                xmax = int(float(data[0])) + 1
        else:
            present_lines = final_lines

        xstep = int( (xmax - xmin) / 5 )
        if xstep <=1:
            xstep = 1
        elif xstep <= 10:
            xstep = 10
        elif xstep <= 40:
            xstep = 20
        else:
            xstep = 50

    fig = plt.figure()
    plt.clf()
    fig, ax=plt.subplots()

    ax.plot(xlist, pvlist, label='PV')
    ax.plot(xlist, mvlist, label='MV')
    ax.set_xlabel("Time [s]", {'fontsize':15})
    ax.set_ylabel("PV, MV", {'fontsize':15})
    ax.legend()
    ax.set_title( appendname + "solved")
#    ax.set_xticks(np.arange(xmin, xmax, step=xstep))

    strFile = "./firstsimulator/static/images/" + appendname + "fixedfunctiongraph.png"
    if os.path.isfile(strFile):
        os.remove(strFile)
        plt.savefig(strFile)
    else:
        plt.savefig(strFile)

    s = io.BytesIO()
    plt.savefig(s,format='png')
    pngvalue = s.getvalue()
    graph = base64.b64encode(pngvalue)
    graph = graph.decode('utf-8')
    s.close()

    fig.clear()
    plt.close(fig)

    return graph

def displaySampleGraph():
    a = 1
    print(a)
