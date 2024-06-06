from django.http import HttpResponse
import pandas as pd
import numpy as np

# 入出力データを取得
# データサンプル周期とデータ数、次数をセットする
# 求める係数行列αを作って初期化する
# 求める係数a0、a1、b0　を用意する
# Y行列を作る
# Ω行列を作る
# Ωの転置かけるΩ
# Ωの転置かけるΩの逆行列
# Ωの転置かけるY
# α　＝　Ωの転置かけるΩの逆行列 ×Ωの転置かけるY
# 係数を求める

def getDataToMatrix(csv_Data):
    baseData = np.array(csv_Data)
    baseData = np.array(baseData[1:, :],dtype=float)

    return baseData

def getDataToMatrix_withFile(file):
    data_dt = 10
    numOfData = 600
    baseData = np.array(pd.read_csv(file, sep=",").values)
    if baseData.shape[0] <= numOfData :
        numOfData = baseData.shape[0] -1
    else:
        numOfData = numOfData

    return baseData

def calcCoefA(baseData, data_dt, numOfData):
    if baseData.shape[0] <= numOfData :
        numOfData = baseData.shape[0] -1
    else:
        numOfData = numOfData

    array_pv = baseData[:numOfData,1]
    array_mv = baseData[:numOfData,2]
    array_pvt = array_pv[2:numOfData].reshape(-1,1)
    array_pvdt = array_pv[1:numOfData-1].reshape(-1,1)
    array_pv2dt = array_pv[0:numOfData-2].reshape(-1,1)
    array_mvt = array_mv[2:numOfData].reshape(-1,1)
    array_omega = np.concatenate([array_pvdt, array_pv2dt, array_mvt],1)
    array_omegaT = array_omega.T
    array_omegaMatmul = array_omegaT @ array_omega
    array_omegapvMatmul = array_omegaT @ array_pvt
    array_alpha = np.linalg.inv(array_omegaMatmul) @ array_omegapvMatmul
    a0 = (array_alpha[0] + array_alpha[1] - 1) / (array_alpha[1] * data_dt * data_dt)
    a1 = -(array_alpha[0] + 2 * array_alpha[1]) / (array_alpha[1] * data_dt)
    b0 = -( array_alpha[2] ) / (array_alpha[1] * data_dt * data_dt)

    return a0, a1, b0




