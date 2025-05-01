import random
import os
import csv
import time
from math import log, exp
import current as cur

def read_measured_data(file_path):
    """CSVファイルから測定データを読み込む"""
    measvgs, measvds, measi = [], [], []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 3:
                measvgs.append(float(row[0]))
                measvds.append(float(row[1]))
                measi.append(float(row[2]))
    return measvgs, measvds, measi

def simulated_annealing(measvgs, measvds, measi, output_file):
    """シミュレーテッド・アニーリングによる最適化処理"""
    IS, RD, KB = 1.45026962144e-03, 0.162747806277, 0.0930109878139
    xstart = [IS, RD, KB]
    xstep = [val / 100 for val in xstart]
    n, m, pn = 500, 110, 3
    t1, t50 = -1.0 / log(0.1), -1.0 / log(0.0001)
    frac = (t50 / t1) ** (1.0 / (n - 1.0))
    xi, xc = list(xstart), list(xstart)
    fc = cur.scaled_costf(xi, measvgs, measvds, measi)
    t, DeltaE_avg, na = t1, 0.0, 1.0
    
    for i in range(n):
        for j in range(m):
            for num in range(pn):
                rand_val = random.random()
                xi[num] = xc[num] + (rand_val - 0.5) * xstep[num]
            
            newfc = cur.scaled_costf(xi, measvgs, measvds, measi)
            DeltaE = abs(newfc - fc)
            
            accept = newfc <= fc or (random.random() < exp(-DeltaE / (DeltaE_avg * t)))
            if accept:
                xc, fc = list(xi), newfc
                na += 1.0
                DeltaE_avg = (DeltaE_avg * (na - 1.0) + DeltaE) / na
        t *= frac
    
    with open(output_file, 'w') as outf:
        outf.write(f'IS = {xc[0]}\nRD = {xc[1]}\nKB = {xc[2]}\n')
    
    return xc

def main():
    start_time = time.time()
    data_file = r"H:\マイドライブ\nmashi\Sample_PCIM\data\Idiode-Vds\rms_results.csv"
    output_file = r"H:\マイドライブ\nmashi\Sample_PCIM\data\Idiode-Vds\Idiode_results.txt"
    
    measvgs, measvds, measi = read_measured_data(data_file)
    optimized_params = simulated_annealing(measvgs, measvds, measi, output_file)
    
    print(f'Optimized Parameters: IS={optimized_params[0]}, RD={optimized_params[1]}, KB={optimized_params[2]}')
    print(f'Elapsed Time: {time.time() - start_time:.2f} s')

if __name__ == "__main__":
    main()
