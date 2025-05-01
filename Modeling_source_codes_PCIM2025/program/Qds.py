import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams["font.size"] = 40
plt.rcParams["axes.labelpad"] = 10
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.linewidth'] = 0.3
plt.rcParams['legend.edgecolor'] = 'black'
plt.rcParams['legend.fancybox'] = False
plt.rcParams['legend.framealpha'] = 1
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['xtick.major.width'] = 1.2
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['ytick.major.width'] = 1.2
plt.rcParams['figure.figsize'] = [8,8]

# define units
m = 1e3
u = 1e6
n = 1e9

def calc_Qds(csv_path):
    """
    Reads a CSV file obtained from a double pulse test for Cds characterization,
    and calculates Qds.
    return:
        DataFrame containing Qds
    """
    df = pd.read_csv(csv_path, skiprows=17)
    df.dropna(axis=1, how='any', inplace=True)

    # define data columns
    df.columns = ["time","Vds_lower", "Vdd","Vghigh_lower", "Vgs_lower",  "Idiode"]

    print(df)

    df["Vds"] = df["Vdd"] - df["Vds_lower"]
    df["Qds"] = (df["Idiode"] * (df["time"] - df["time"].shift(1)).fillna(0)).cumsum()
    df["Qds"] = -df["Qds"]

    df = df[df["time"] <= 2.8e-6]

    return df

def Qds_func(Vds, CDSO, CDSV, CDSM):
    """
    Qds model equation. CDS0, CDSV, CDSM are model parameters.
    Return:
        Qds at given Vds
    """
    return CDSO * CDSV / (1.0 - CDSM) * (1.0 + Vds / CDSV) ** (1.0 - CDSM) - CDSO * CDSV / (1.0 - CDSM)

def Qds_modeling(df, csv_folder, csv_file):
    """
    Scale Vds and Qds before fitting.
    Return:
        DataFrame and fitting parameters CDSO, CDSV, CDSM
    """
    # data scaling
    Vds_max = df["Vds"].max()
    Qds_max = df["Qds"].max()
    Vds_scaled = df["Vds"] / Vds_max
    Qds_scaled = df["Qds"] / Qds_max

    # initial guess for curve fitting
    initial_guess = [1, 1, 0.1]
    
    try:
        popt, pcov = curve_fit(Qds_func, Vds_scaled, Qds_scaled, p0=initial_guess)
        df["Qds_model"] = Qds_func(Vds_scaled, *popt) * Qds_max


        log_file_path = os.path.join(csv_folder, f"Qds_results.txt")
        with open(log_file_path, 'w') as log_file:
            log_file.write(f"CDSO = {popt[0]}\n")
            log_file.write(f"CDSV = {popt[1]}\n")
            log_file.write(f"CDSM = {popt[2]}\n")
    except RuntimeError as e:
        print(f"Fit failed: {e}")
        df["Qds_model"] = np.nan

    fig2 = plt.figure()
    bx = fig2.add_subplot(111)
    bx.plot(df["Vds"], df["Qds"] * n, label=r'Measurement',color="gray",alpha=1,linewidth = 3)
    bx.plot(df["Vds"], df["Qds_model"] * n, label=r'Model',color="tab:blue",alpha=1,linewidth = 3)
    bx.set_ylim(0,30)
    bx.set_xlabel(r'$V_\mathrm{ds}$ [V]')
    bx.set_ylabel(r'$Q_\mathrm{ds}$ [nC]')
    bx.legend(loc="lower right",fontsize=25)
    plt.xlim(0,100)
    plt.ylim(0,20)
    plt.xticks(np.arange(0,120,20))
    # plt.tight_layout()
    plt.subplots_adjust(left=0.15)
    bx.tick_params(axis='x', pad=10)  # x軸目盛と軸の距離を10ポイントに設定
    bx.tick_params(axis='y', pad=15)  # y軸目盛と軸の距離を15ポイントに設定
    # fig2.savefig(os.path.join(csv_folder, "Vds-Qds.pdf"), bbox_inches='tight')
    plt.show()

    return df, popt

def main():
    csv_folder = r"H:\マイドライブ\nmashi\Sample_PCIM\data"
    csv_file = r"Qds_Vgs=20_Vdd=100_000_ALL"
    csv_path = os.path.join(csv_folder, csv_file + ".csv")
    df = calc_Qds(csv_path)
    df, popt = Qds_modeling(df, csv_folder, csv_file)
    print("CDSO =", popt[0], "CDSV =", popt[1], "CDSM =", popt[2])
    print(popt)

if __name__ == "__main__":
    main()
