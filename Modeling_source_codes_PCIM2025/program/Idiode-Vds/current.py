import sys
import os
import time
import numpy as np
from math import log, exp, pow, sqrt, tanh

def I(xi, Vgs, Vds):
    # # モデルパラメータ
    IS = xi[0]
    RD = xi[1]
    KB = xi[2]

    # Ids = IS * (np.exp((Vds - RD * Ids)/(KB)) - 1)

    # return Ids
    # IS = xi[0]
    # N  = xi[1]
    # RS = xi[2]
    gmin = 1e-12

    rmin = 0.0
    rmax = 1.0

    for i in range(30):
        rtmp = (rmin+rmax)/2.0
        Vdr = rtmp * Vds

        if Vdr<0.0:
            Vdr=0.0

        Ids = IS*(exp((Vdr)/RD)-1.0)
        Id = Ids + gmin*Vds

        if Id>(1.0-rtmp)*Vds/KB:
            rmax = rtmp
        elif Id<(1.0-rtmp)*Vds/KB:
            rmin = rtmp
        else:
            break
    
    return Id

# def I(xi, Vgs, Vds):
#     # # モデルパラメータ
#     IS = xi[0]
#     RD = xi[1]
#     KB = xi[2]

#     Id = IS * (np.exp((RD*Vds)/(KB)) - 1)
    
#     return Id

def costf(xi, *args):
    obj = 0.0
    measvgs, measvds, measi = args
    for i in range(len(measvgs)):
        obj += (I(xi, measvgs[i], measvds[i]) - measi[i])**2
    return np.sqrt(obj / len(measvgs))

def _costf(xi, *args):
    obj = 0.0
    measvgs, measvds, measi = args
    a = max(measi)
    b = min(measi)
    for i in range(len(measvgs)):
        Id = max(I(xi, measvgs[i], measvds[i]), 1e-12)
        Id_sim_lin = Id/a + np.log(Id/a)/np.log(a/b)
        Id_mea_lin = abs(measi[i])/a + np.log(abs(measi[i])/a)/np.log(a/b)
        obj += (Id_sim_lin - Id_mea_lin)**2
    return obj

def improved_costf(xi, *args):
    obj = 0.0
    measvgs, measvds, measi = args
    
    # ロバストなエラーメトリックの使用
    for i in range(len(measvgs)):
        simulated_Id = I(xi, measvgs[i], measvds[i])
        # 外れ値に対してロバストな絶対誤差
        obj += np.abs(simulated_Id - measi[i]) / np.max(measi)
    
    return obj / len(measvgs)

def scaled_costf(xi, *args):
    obj = 0.0
    measvgs, measvds, measi = args
    
    # スケーリングと正規化
    Vds_max = np.max(measvds)
    Id_max = np.max(measi)
    
    for i in range(len(measvgs)):
        simulated_Id = I(xi, measvgs[i], measvds[i])
        # スケールされた二乗誤差
        obj += ((simulated_Id - measi[i]) / Id_max)**2
    
    return np.sqrt(obj / len(measvgs))

def weighted_costf(xi, *args):
    obj = 0.0
    measvgs, measvds, measi = args
    
    # 重み付け
    weight_low_vgs = 10.0  # 低い Vgs の重み
    weight_high_vgs = 1.0 # 高い Vgs の重み
    
    for i in range(len(measvgs)):
        simulated_Id = I(xi, measvgs[i], measvds[i])
        if measvgs[i] <= 6:  # 例として、Vgsが6V未満を低いVgsとする
            weight = weight_low_vgs
        else:
            weight = weight_high_vgs
        # 重み付けされた二乗誤差
        obj += weight * (simulated_Id - measi[i])**2
    
    return np.sqrt(obj / len(measvgs))

if __name__ == "__main__":
    measvgs = []
    measvds = []
    measi = []

    fname = ["./average_data"]
    f = fname[0] + '.txt'

    with open(f, 'r') as file:
        for line in file:
            sline = line.split()
            if len(sline) != 0:
                measvgs.append(float(sline[0]))
                measvds.append(float(sline[1]))
                measi.append(float(sline[2]))

    argc = len(sys.argv)

    # 初期パラメータ
    IS = 0.00396019129719
    RD = 0.470145669082
    KB = 0.0612327629053

    if argc == 1:
        xstart = [IS, RD, KB]
    else:
        xstart = np.loadtxt(sys.argv[1])

    with open('idvd.log', 'w') as outf:
        for i in range(len(measvgs)):
            current = I(xstart, measvgs[i], measvds[i])
            print(measvgs[i], measvds[i], current, measi[i])
            print(str(measvgs[i]), str(measvds[i]), str(current), str(measi[i]), file=outf)

    # コスト関数のテスト
    test_cost = weighted_costf(xstart, measvgs, measvds, measi)
    print('Test Cost (Weighted):', test_cost)
