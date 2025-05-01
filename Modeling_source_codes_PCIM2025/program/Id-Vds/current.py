import sys
import os
import time

from math import log, exp, pow, sqrt, tanh
import numpy as np


def I(xi, Vgs, Vds):
    """
    Drain current model equation

    Return:
        current at given Vgs and Vds
    """
    VTH = xi[0]
    R1 = xi[1]
    DELTA = xi[2]
    K1 = xi[3]
    CLM = xi[4]
    MOB = xi[5]
    MOVTH = xi[6]
    BBB = xi[7]
    J1 = xi[8]
    M1 = xi[9]
    N1 = xi[10]

    Vp = Vgs - VTH

    # Vdssat と Idsat の計算
    if(Vp>0):
        Vdssat = J1*pow(Vp,M1)
    else:
        Vdssat = 0
    if(Vp>0):
        Idsat = K1*pow(Vp,N1)
    else:
        Idsat = 0

    rmin = 0.0
    rmax = 1.0

    for i in range(30):
        rtmp = (rmin + rmax) / 2.0
        Vds1 = rtmp * Vds
        Vdg = Vds1 - Vgs

        if DELTA < 0.0:
            if Vds1<Vp:
                Vdsmod=Vds1
            else:
                Vdsmod=Vp
        elif Vp < 0.0:
            Vdsmod = Vds1
        else:
            Vdsmod = Vds1 / pow(1.0 + pow(Vds1 / Vdssat, DELTA), 1.0 / DELTA)

        Ids_tmp=Idsat*(2-Vdsmod/Vdssat)*(Vdsmod/Vdssat)*0.5*(1+tanh((Vgs-VTH)/BBB))
        Ids_tmp = Ids_tmp*(1.0+CLM*Vds)
        if Vgs>MOVTH:
            Ids_tmp = Ids_tmp/(1.0+MOB*(Vgs-MOVTH))
        Ids = Ids_tmp

        if Ids>(1.0-rtmp)*Vds/R1:
            rmax = rtmp
        if Ids<(1.0-rtmp)*Vds/R1:
            rmin = rtmp
        else:
            break

    return Ids


def costf(xi, *args):
    """
    Cost function for fitting

    Return:
        objective function value
    """
    obj = 0.0
    measvgs,measvds,measi = args
    for i in range(len(measvgs)):
        obj = obj + ((I(xi,measvgs[i],measvds[i]))-(measi[i]))**2
    obj1 = sqrt(obj/len(measvgs))
    obj = 0
    for i in range(len(measvgs)):
        obj = obj + ((np.log(I(xi,measvgs[i],measvds[i])))-np.log(measi[i]))**2
    obj2 = sqrt(obj/len(measvgs))
    return obj1+obj2


def _costf(xi, *args):
    obj = 0.0
    measvgs,measvds,measi = args
    a = max(measi)
    b = min(measi)
    for i in range(len(measvgs)):
        if I(xi,measvgs[i],measvds[i]) <= 0.0:
            ids = 1e-12
        else:
            ids = I(xi,measvgs[i],measvds[i])
        #print(('hoge',ids, a, b, a/b))
        ids_sim_lin = ids/a + log(ids/a)/log(a/b)
        ids = abs(measi[i])
        ids_mea_lin = ids/a + log(ids/a)/log(a/b)
        obj = obj + (ids_sim_lin-ids_mea_lin)**2
    return obj


if __name__ == "__main__":
    """
    Edit:
        set initial values
    """
    measvgs=[]
    measvds=[]
    measi=[]

    fname=["./average_data"]
    fn = len(fname)
    f=str(fname[0])+'.txt'
    del measvgs[:]
    del measvds[:]
    del measi[:]


    for line in open(f):
        sline = line.split()
        if len(sline)!=0:
            measvgs.append(float(sline[0]))
            measvds.append(float(sline[1]))
            measi.append(float(sline[2]))

    argc = len(sys.argv)

    VTH = 3.11249045472
    R1 = 0.000955214004347
    DELTA = 1.65239229904
    K1 = 0.0543592680141
    CLM = 0.00196168142255
    MOB = 0.568818520078
    MOVTH = 0.73798181621
    BBB = 0.456297965688
    J1 = 0.196539882027
    M1 = 1.65510599907
    N1 = 3.59798353238

    if argc == 1:
        xstart = [
            VTH,
            R1,
            DELTA,
            K1,
            CLM,
            MOB,
            MOVTH,
            BBB,
            J1,
            M1,
            N1
        ]
    else:
        xstart = np.loadtxt(sys.argv[1])

    count=1

    fff = 'idvd.log'
    outf = open(fff, 'w')
    for i in range(len(measvgs)):
        current = I(xstart,measvgs[i],measvds[i])
        print(measvgs[i],measvds[i],current,measi[i])
        print(str(measvgs[i]),str(measvds[i]),str(current),str(measi[i]), file = outf)
    #    if count%21 == 0:
    #        print('')
        count=count+1
        #print(costf(xstart,measvgs,measvds,measi))



