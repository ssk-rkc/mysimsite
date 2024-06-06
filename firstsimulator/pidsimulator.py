import os
import csv
import datetime
import time


def write_csv(data):
    datas = [data]
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "data/data.csv")
    with open(filename,'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(datas)

# PID演算処理
# PV、SV、PID定数、からMVを算出する
# 計算終了時間から計算回数を算出　→forLoopcountLim
#
# MVとPVの前回値、前々回値から　PVを算出する
#
# 値の保持と更新
#
# Time,PV,MV をcsvに保存
# Time,PV,MV をグラフ描画関数に返す
#
#
def generateControlData( ctrlSetting, plantSetting, simSetting ):
    sv    = int( ctrlSetting['SV'] )
    contP = int( ctrlSetting['P'] )
    contI = int( ctrlSetting['I'] )
    contD = int( ctrlSetting['D'] )
    contDGain =  int( contI / contD )

    initPv          = 25
    stopTime        = float(simSetting['StopTime'])
    dt              = float(simSetting['SampleTime'])
    nData           = int(stopTime / dt)
    plantDt         = dt



    sv      = sv -initPv
    pv      = 0
    prevE   = 0

    mv      = 0
    mvI     = 0
    mvD     = 0

    nTime   = int(stopTime / dt)

    a0 = float( plantSetting['coef1'] )
    a1 = float( plantSetting['coef2'] )
    b0 = float( plantSetting['coef3'] )

    Vout = 0
    prevVout = 0
    moreprevVout = 0
    PlantTime = int( dt/plantDt )

    solvData = []
    for iTime in range(nTime):
        for iPlantTime in range(PlantTime):
            plantIn = mv * 0.01 * 100
            Vout = ( 1 / ( 1 + a1 * plantDt + a0 * pow( plantDt, 2 ))) * ( (b0 * pow(plantDt, 2 )  * plantIn) + (a1 * plantDt + 2) * prevVout - moreprevVout )
            moreprevVout = prevVout
            prevVout = Vout
            pv = Vout

        Kp = 100 / (contP + 0.000001)
        e = sv - pv

        mvP = Kp * e
        isEInPropBand = abs(e) <= contP
        if int( ctrlSetting['ARW'] )==0:
            doARW = False
        else:
            doARW = True

        if contI <= 0:
            mvI = 0
        elif doARW & (not isEInPropBand):
            mvI = 0
        else:
            mvI = Kp / ( contI * e * dt ) +mvI

        mvD = (Kp * contD * (e-prevE) + contD * contDGain * mvD)/(dt + contD * contDGain)
        mv = mvP + mvI + mvD
        mv = min( max( mv, 0), 100)

        Time = iTime * dt
        PV = pv + initPv
        MV = mv
        MVP = mvP
        MVI = mvI
        MVD = mvD
        row = [Time, PV, MV, MVP, MVI, MVD]
        solvData.append(row)

#        list_data = {
#            "Time"  : iTime * dt,
#            "PV"    : pv + initPv,
#            "SV"    : sv + initPv,
#            "MV"    : mv
#            "MVp"   : mvP,
#            "MVi"   : mvI,
#            "MVd"   : mvD
#        }
 #       solvData.append(list_data)
        prevE = e

    return solvData
