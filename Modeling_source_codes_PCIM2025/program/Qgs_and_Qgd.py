
import pandas as pd
import os
import numpy as np
import random
import time
import matplotlib.pyplot as plt
import sys
from scipy.optimize import curve_fit
from scipy.stats import gaussian_kde

## matplotlib settings ##
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

## convert SI units ##
m = 1e3
u = 1e6
n = 1e9


def calc_Qg(csv_path, Resistance):
    """
    Read the CSV file obtained from the double pulse test and calculate Qg during turn-on and turn-off.
    return:
        DataFrames with calculated results added (entire data, turn-on, turn-off)
    """
    ## Skip metadata and read the CSV into a DataFrame
    df = pd.read_csv(csv_path, skiprows=17)
    df.dropna(axis=1, how='any', inplace=True)
    
    ## Update columns to match the data being read ##
    #       time:time, v_ds:Drain-Source voltage, Vdd:Power supply voltage
    #       v_ghigh:gate driver output voltage, v_gs:Gate Source voltage, I_d:Drain current
    df.columns = ["time", "v_ds", "Vdd" , "v_ghigh", "v_gs", "I_d"]

    ## Remove data after the 2nd pulse has fully risen ##
    df = df[df["time"] <= 14e-6]
    
    ## Calculate drain current, gate-drain voltage, and gate charge ##
    df["I_g"] = (df["v_ghigh"] - df["v_gs"]) / Resistance
    df["v_gd"] = df["v_ds"] - df["v_gs"]
    df["Q_g"] = (df["I_g"] * (df["time"] - df["time"].shift(1)).fillna(0)).cumsum()

    ## Calculate the maximum value of the drain current ##
    max_idx = df["I_g"].idxmax()
    min_idx = df["I_g"].idxmin()
    
    ## Adjust the turn-on and turn-off regions by observing plots using matplotlib ##
    #       In this sample, the rising edge corresponds to 0.5% of the total data, 
    #       and the falling edge corresponds to 20% of the total data.
    up_percent = int(len(df) * 0.005)
    down_percent = int(len(df) * 0.2)
    
    ## separate turn-on and turn-off dataframe
    df_on = df.iloc[max(0, max_idx - up_percent):max(0, max_idx + int(down_percent*1.4))].copy()
    df_off = df.iloc[max(0, min_idx - up_percent):max(0, min_idx + down_percent)].copy()
    df_on["Q_g"] = (df_on["I_g"] * (df_on["time"] - df_on["time"].shift(1)).fillna(0)).cumsum()
    df_off["Q_g"] = (df_off["I_g"] * (df_off["time"] - df_off["time"].shift(1)).fillna(0)).cumsum()
    df_off["Q_g"] = df_off["Q_g"] - min(df_off["Q_g"])

    return df, df_on, df_off




def Qgs_modeling(df):
    """
    Fit Qgs as a linear function. This is because we assume that Cgs is a constant.
    return:
        Fitting parameters CGSO, G      
    """
    ## Fit with a linear equation
    CGSO,G=np.polyfit(df["v_gs"],df["Q_g"],1)    
    return CGSO,G




def Qdg_func(v_gd, COXD, VJ, CDGO, B,smooth,tanj,QC):
    """
    Calculate Cgd 
    return:
        Qgd
    """

    ## Restrict the range of smooth ##
    smooth = max(1, min(smooth, 10))

    ## Calculate Qgd
    Qdg1 = np.where(v_gd < -0.5 * VJ,
            -2 * CDGO * np.sqrt(0.5 * VJ) - B,
            -2 * CDGO * np.sqrt(v_gd + 0.5 * VJ) - B)
    Qdg2 = COXD * v_gd - 2 * CDGO * np.power(0.5 * VJ, 0.5) + 0.5 * VJ * COXD -QC
    smooth_Qdg = 0.5 + 0.5 * np.tanh((v_gd - (tanj)) / 10)
    Qgd = -Qdg1 * smooth_Qdg - Qdg2 * (1 - smooth_Qdg)

    return Qgd
    



def sample(df, vgd_step=0.05, points_to_average=100):
    """
    Vgd does not change linearly with time, and some data points are concentrated in certain regions along vgd axis.
    This affect the fitting result. Therefore, the data is sampled to ensure a more even distribution of data points.
    return:
            A DataFrame containing the sampled data.
    """
    ## Vgdの最大値と最小値 ##
    min_value = df['v_gd'].min()
    max_value = df['v_gd'].max()
    
    ## Vgdをvgd_stepごとにサンプリングして時間的な偏りを低減 ##
    sample_vgd_values = np.arange(min_value, max_value, vgd_step)
    
    ## 各サンプリングポイントで平均化した結果を格納するリスト ##
    averaged_rows = []
    
    ## vgd_stepごとに近いVgdを探して格納 ##
    for vgd in sample_vgd_values:

        ## 指定したv_gdに最も近い点を探す
        nearest_index = (df['v_gd'] - vgd).abs().idxmin()
        first_index = df.index[0]
        nearest_index = nearest_index - first_index

        ## nearest_index がデータの範囲内にあるか確認
        if nearest_index < 0 or nearest_index >= len(df):
            print(f"Error: nearest_index {nearest_index} is out of bounds.")
            continue
        
        ## 前後 points_to_average のデータを取得
        #       0未満にならないように
        start_index = max(nearest_index - points_to_average, 0)  
        #       データの範囲を超えないように
        end_index = min(nearest_index + points_to_average + 1, len(df))  

        ## デバッグ用出力 ##
        # print("--------")
        # print(f"v_gd: {vgd}")
        # print(f"Nearest index: {nearest_index}")
        # print(f"Start index: {start_index}")
        # print(f"End index: {end_index}")

        # 前後のpoints_to_averageを平均化
        subset = df.iloc[start_index:end_index]

        ## 結果をリストに追加 ##
        averaged_row = subset.mean()
        averaged_rows.append(averaged_row)
        
    ## 結果をデータフレームに変換 ##
    df_sample = pd.DataFrame(averaged_rows).reset_index(drop=True)
    df_sample = df_sample.sort_values(by=["v_gd"])

    return df_sample




def Qgd_modeling(df,CGSO,G):
    """
    Perform fitting of Qgd using model equations.
    return:
        fitting parameters: COXD, VJ, CDGO, B, smooth, tanj, QC
    """

    ## Qgd ????
    df = df[df["v_gd"] <= 80] 
    
    ## Vgd sampling 
    df_sample = sample(df)

    ## Qgd fitting
    popt, pcov = curve_fit(
        Qdg_func, 
        df_sample["v_gd"], 
        df_sample["Q_gd"], 
        bounds=([-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf], [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf])
    )

    return df, popt




def Graph(show,save,df,df_input,df_output,MODE,df_on,df_off,csv_folder):
    """
    visualize everything
    """

    ## Qg vs Qgs_model ##
    fig1 = plt.figure()
    ax = fig1.add_subplot(111)
    ax.plot(df_input["v_gs"], df_input["Q_g"]*n, label=r'Measurement($Q_\mathrm{g}$)',color="gray",alpha=1,linewidth = 3)
    ax.plot(df_input["v_gs"], df_input["Qgs_model"]*n, label=r'Model($Q_\mathrm{gs}$)',color="tab:blue",alpha=1,linewidth = 3)
    ax.set_xlabel(r'$V_\mathrm{gs}$ [V]')
    ax.set_ylabel(r'$Q_\mathrm{g}$,$Q_\mathrm{gs}$ [nC]')
    ax.set_xticks(np.arange(0,25,5))
    ax.legend(loc="lower right",fontsize=25)
    # plt.tight_layout()
    plt.subplots_adjust(left=0.15)
    ax.tick_params(axis='x', pad=10)  # x軸目盛と軸の距離を10ポイントに設定
    ax.tick_params(axis='y', pad=15)  # y軸目盛と軸の距離を15ポイントに設定

    ## Qgd vs Qgd_model ##
    fig4 = plt.figure()
    bx = fig4.add_subplot(111)
    # bx.plot(df_output["v_gd"], df_output["Q_g"]*n, label=r'$Q_\mathrm{g}$('+MODE+r')')
    bx.plot(df_output["v_gd"], df_output["Q_gd"]*n, label=r'Measurement',color="gray",alpha=1,linewidth = 3)
    # bx.plot(df_output["v_gd"], df_output["Qgs_model"]*n, label=r'$Q_\mathrm{gs}$('+MODE+r')')
    # bx.plot(df_input["v_gd"], df_input["Qgd_b"]*n, label=r'$Q_\mathrm{gd-b}$('+MODE+r')')
    # bx.plot(df_input["v_gd"], df_input["Qgd_c"]*n, label=r'$Q_\mathrm{gd-c}$('+MODE+r')')
    bx.plot(df_output["v_gd"], df_output["Qgd_model_tanh"]*n, label=r'Model',color="tab:blue",alpha=1,linewidth = 3)
    # bx.plot(df_input["v_gd"],df_input["Qgd_c"]*n)
    # bx.plot(df_input["v_gd"],df_input["Qgd_b"]*n)
    # bx.plot(df_input["v_gd"],df_input["Qgd_model_tanh"]*n,label=r'$Q_\mathrm{gd-Model}$('+MODE+r')')
    bx.set_xlabel(r'$V_\mathrm{gd}$ [V]')
    bx.set_ylabel(r'$Q_\mathrm{gd}$ [nC]')
    bx.vlines(-1.355, -1, 30, colors='tab:orange', linestyle='--',label=r"$-0.5\cdot \mathbf{VJ}$")
    bx.legend(fontsize=25)
    plt.subplots_adjust(hspace=0.4)
    # plt.tight_layout()
    plt.subplots_adjust(left=0.15)
    bx.tick_params(axis='x', pad=10)  # x軸目盛と軸の距離を10ポイントに設定
    bx.tick_params(axis='y', pad=15)  # y軸目盛と軸の距離を15ポイントに設定
    bx.set_xticks(np.arange(-20,100,20))
    bx.set_xlim(-20,80)
    bx.set_ylim(0,25)
    
    
    ## Vgs-Vds-Qg ##
    # fig2 = plt.figure()
    # cx = fig2.add_subplot(111, projection='3d')
    # cx.plot(df_on["v_gd"], df_on["v_gs"], df_on["Q_g"]*n, label=r'$Q_\mathrm{g}$(on)', color='r')
    # cx.plot(df_off["v_gd"], df_off["v_gs"], df_off["Q_g"]*n, label=r'$Q_\mathrm{g}$(off)', color='b')
    # # cx.plot(df_input["v_gd"], df_input["v_gs"], df_input["Q_g"]*n, label=r'$Q_\mathrm{g}$('+MODE+r')', color='b')
    # cx.set_xlabel(r'$V_\mathrm{gd}$ [V]')
    # cx.set_ylabel(r'$V_\mathrm{gs}$ [V]')
    # cx.set_zlabel(r'$Q_\mathrm{g}$ [nC]')
    # cx.legend()

    ## time-Ig ターンオン、ターンオフの領域決めに必要 ##
    # fig3 = plt.figure()
    # dx = fig3.add_subplot(111)
    # dx.plot(df["time"]*u, df["I_g"]*m, label=r"$I_\mathrm{g}$")
    # dx.plot(df_on["time"]*u, df_on["I_g"]*m, color='red', label=r"$I_\mathrm{g}$(on)",linestyle = "--")
    # dx.plot(df_off["time"]*u, df_off["I_g"]*m, color='green', label=r"$I_\mathrm{g}$(off)",linestyle = "--")
    # dx.set_xlabel(r"Time [$\mu$s]")
    # dx.set_ylabel(r"$I_\mathrm{g}$ [mA]")
    # dx.legend()

    ## グラフの表示・保存設定
    if show == "y":
        plt.show()
    if save == "y":
        fig1.savefig(os.path.join(csv_folder, "Vgs-Qgs_"+MODE+".pdf"), bbox_inches='tight')
        # fig2.savefig(os.path.join(csv_folder, "Vgs-Vds-Qg.png"))
        # fig3.savefig(os.path.join(csv_folder, "Time-Ig.png"))
        fig4.savefig(os.path.join(csv_folder, "Vgd-Qgd_"+MODE+".pdf"), bbox_inches='tight')





def save_results_to_txt(csv_folder, results):
    """
        Save the fitting results as a text file in the CSV folder.
        """

    output_path = os.path.join(csv_folder, "Qgs_and_Qgd_results.txt")
    with open(output_path, 'w') as f:
        for mode, res in results.items():
            f.write(f"Mode: {mode}\n")
            f.write(f"CGSO = {res['CGSO']}\n")
            f.write(f"G = {res['G']}\n")
            f.write(f"COXD = {res['COXD']}\n")
            f.write(f"CDGO = {res['CDGO']}\n")
            f.write(f"VJ = {res['VJ']}\n")
            f.write(f"QB = {res['B']}\n")
            f.write(f"smooth = {res['smooth']}\n")
            f.write(f"tanj = {res['tanj']}\n")
            f.write(f"QC = {res['QC']}\n")
            f.write("="*50 + "\n")





def main():
    csv_folder = r"..\data" # the parent folder where the CSV files are located
    csv_file = r"Qg_Vgs=20_Vdd=100_000_ALL"
    csv_path = os.path.join(csv_folder, csv_file + ".csv")
    Resistance = 510 

    ## Graph display and save settings, set to "y" if needed ##
    show, save = "y", "n"

    ## Dictionary to store results for both ON and OFF modes ##
    results = {}

    for MODE in ["on", "off"]:
        df, df_on, df_off = calc_Qg(csv_path, Resistance)

        ## 区間AとBの切り替わりを手動で決定ー＞後に自動化予定 ##
        if MODE == "on":
            on_kukanA = 1700
            df_on_kukanA = df_on[:on_kukanA]
            df_kukanA = df_on_kukanA
            df_input = df_on
        elif MODE == "off":
            off_kukanA = 6000
            df_off_kukanA = df_off[off_kukanA:]
            df_kukanA = df_off_kukanA
            df_input = df_off
        else:
            print('MODE needs to be either "on" or "off".')
            print("Forcing the program to terminate...")
            sys.exit()

        CGSO, G = Qgs_modeling(df_kukanA)
        df_input["Qgs_model"] = CGSO * df_input["v_gs"] + G
        df_input["Q_gd"] = df_input["Q_g"] - (CGSO * df_input["v_gs"] + G)

        df_output, popt = Qgd_modeling(df_input, CGSO, G)

        COXD, VJ, CDGO, B ,smooth,tanj,QC= popt[0], popt[1], popt[2], popt[3],popt[4],popt[5],popt[6]
        
        df_output["Qgd_model_tanh"] = Qdg_func(df_output["v_gd"], COXD, VJ, CDGO, B,smooth,tanj,QC)

        results[MODE] = {
            "CGSO": CGSO,
            "G": G,
            "COXD": COXD,
            "CDGO": CDGO,
            "VJ": VJ,
            "B":B,
            "smooth":smooth,
            "tanj":tanj,
            "QC":QC
        }

        print(f"{MODE.upper()} Mode Results:")
        print(f"CGSO = {CGSO}, G = {G}")
        print(f"COXD = {COXD}, CDGO = {CDGO}")
        print(f"VJ = {VJ}, CNT = {-0.5 * VJ}")
        print(f"smooth = {smooth}")
        print(f"tanj = {tanj}")
        print(f"QC = {QC}")

        Graph(show, save, df, df_input, df_output, MODE, df_on, df_off, csv_folder)

    save_results_to_txt(csv_folder, results)




if __name__ == "__main__":
    main()
