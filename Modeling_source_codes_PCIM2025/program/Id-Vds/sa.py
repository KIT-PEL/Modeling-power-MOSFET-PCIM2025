import random
import time
import csv
import os
from math import log, exp
import current as cur

def read_csv_data(fname):
    """ CSVファイルからデータを読み込む """
    measvgs, measvds, measi = [], [], []
    with open(fname, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 3:
                measvgs.append(float(row[0]))
                measvds.append(float(row[1]))
                measi.append(float(row[2]))
    return measvgs, measvds, measi

def simulated_annealing(xstart, xstep, xmax, xmin, measvgs, measvds, measi, n=200, m=100):
    """ 焼きなまし法によるパラメータ最適化 """
    pn = len(xstart)
    p1, p50 = 0.1, 0.0001
    t1, t50 = -1.0 / log(p1), -1.0 / log(p50)
    frac = (t50 / t1) ** (1.0 / (n - 1.0))
    
    xi, xc = list(xstart), list(xstart)
    fc = cur.costf(xi, measvgs, measvds, measi)
    t, DeltaE_avg, na = t1, 0.0, 1.0
    
    for i in range(n):
        print(f'Cycle: {i}, Object: {fc}')
        for j in range(m):
            for num in range(pn):
                xi[num] = xc[num] + (random.random() - 0.5) * xstep[num]
                if not (xmin[num] <= xi[num] <= xmax[num]):
                    xi[num] = xc[num]
            
            newfc = cur.costf(xi, measvgs, measvds, measi)
            DeltaE = abs(newfc - fc)
            accept = newfc <= fc or (random.random() < exp(-DeltaE / (DeltaE_avg * t)))
            
            if accept:
                xc, fc = list(xi), newfc
                na += 1.0
                DeltaE_avg = (DeltaE_avg * (na - 1.0) + DeltaE) / na
        
        t *= frac
    return xc, fc

def write_results(outfile, xc, fc):
    """ 結果をファイルに書き出す """
    with open(outfile, 'w') as outf:
        print(outfile)
        params = ["VTH", "RS", "DELTA", "K", "CLM", "MOB", "MOVTH", "SMOOTH", "J", "M", "N"]
        for name, value in zip(params, xc):
            print(f'{name} = {value}', file=outf)
        print(fc, file=outf)

def main():
    fname = r"H:\マイドライブ\nmashi\Sample_PCIM\data\Id-Vds\rms_results.csv"
    outfile = r"H:\マイドライブ\nmashi\Sample_PCIM\data\Id-Vds\Id_results.txt"
    
    xstart = [3.11249045472, 0.000955214004347, 1.65239229904, 0.0543592680141, 0.00196168142255,
              0.568818520078, 0.73798181621, 0.456297965688, 0.196539882027, 1.65510599907, 3.59798353238]
    xstep = [x / 100.0 for x in xstart]
    xmax = [x * 10 if i == 0 else x * 1000 for i, x in enumerate(xstart)]
    xmin = [0] * len(xstart)
    
    start_time = time.time()
    measvgs, measvds, measi = read_csv_data(fname)
    xc, fc = simulated_annealing(xstart, xstep, xmax, xmin, measvgs, measvds, measi)
    write_results(outfile, xc, fc)
    
    print(f'elapsed_time: {time.time() - start_time} (s)')

if __name__ == "__main__":
    main()