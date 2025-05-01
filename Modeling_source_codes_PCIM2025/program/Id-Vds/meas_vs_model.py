import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from data_loader import load_data
from RMS import compute_rms

# プロットの設定（変更なし）
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
plt.rcParams['figure.figsize'] = [8, 8]

def load_parameters(filename):
    """
    パラメータファイルの読み込み。

    return:
        パラメータのリスト
    """
    params = {}
    with open(filename, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=')
                params[key.strip()] = float(value.strip())
    return params

def calculate_id(Vds, Vgs, params):
    """
    電流の計算式。

    return:
        電流値
    """
    Vgs = float(Vgs)
    Vp = Vgs - params["VTH"]

    # Vdssat と Idsat の計算
    if(Vp>0):
        Vdssat = params["J"]*pow(Vp,params["M"])
    else:
        Vdssat = 0
    if(Vp>0):
        Idsat = params["K"]*pow(Vp,params["N"])
    else:
        Idsat = 0

    rmin = 0.0
    rmax = 1.0

    for i in range(30):
        rtmp = (rmin + rmax) / 2.0
        Vds1 = rtmp * Vds
        Vdg = Vds1 - Vgs

        if params["DELTA"] < 0.0:
            if Vds1<Vp:
                Vdsmod=Vds1
            else:
                Vdsmod=Vp
        elif Vp < 0.0:
            Vdsmod = Vds1
        else:
            Vdsmod = Vds1 / pow(1.0 + pow(Vds1 / Vdssat, params["DELTA"]), 1.0 / params["DELTA"])


        Ids_tmp=Idsat*(2-Vdsmod/Vdssat)*(Vdsmod/Vdssat)*0.5*(1+np.tanh((Vgs-params["VTH"])/params["SMOOTH"]))
        # CLM MOBdegradation
        Ids_tmp = Ids_tmp*(1.0+params["CLM"]*Vds)
        if Vgs>params["MOVTH"]:
            Ids_tmp = Ids_tmp/(1.0+params["MOB"]*(Vgs-params["MOVTH"]))
        Ids = Ids_tmp

        if (Ids>(1.0-rtmp)*Vds/params["RS"]).any():
            rmax = rtmp
        if (Ids<(1.0-rtmp)*Vds/params["RS"]).any():
            rmin = rtmp
        else:
            break

    return Ids

def _calculate_id(Vds, Vgs, params):
    Vgs = float(Vgs)
    Vds_sat = params['J'] * (Vgs - params['VTH']) ** params['M']
    Id_sat = params['K'] * (Vgs - params['VTH']) ** params['N']
    Vds_int = Vds - params['RS'] * Id_sat
    Vds_mod = Vds_int / (1 + (Vds_int / Vds_sat) ** params['DELTA']) ** (1/params['DELTA'])
    Id = Id_sat / 2 * (2 - Vds_mod / Vds_sat) * Vds_mod / Vds_sat * (1 + np.tanh((Vgs - params['VTH']) / params['SMOOTH'])) * ((1 + params['CLM'] * Vds) / (1 + params['MOB'] * (Vgs - params['MOVTH'])))
    return Id

def plot_iv_curve(data, base_dir, params):
    """
    モデルと実験データを同じ平面にプロット。
    """
    fig, ax = plt.subplots()
    cmap = plt.get_cmap('tab10')
    # 文字列の Vgs 値を数値に変換してソート
    vgs_values = sorted(data.keys(), key=lambda x: float(x))
    
    # Model データを先にプロット
    Vds = np.linspace(0, 100, 1000)
    for i, vgs in enumerate(vgs_values):
        Id = calculate_id(Vds, vgs, params)
        ax.plot(Vds, Id, linestyle='-', color="black", zorder=1)  # zorderを小さく設定

    # Experiment データを後でプロット
    for i, vgs in enumerate(vgs_values):
        vdd_dict = data[vgs]
        rms_vds_list = []
        rms_id_list = []
        for vdd, df in vdd_dict.items():
            rms_vds, rms_id, _, _ = compute_rms(df)
            rms_vds_list.append(rms_vds)
            rms_id_list.append(rms_id)
        
        ax.plot(rms_vds_list, rms_id_list, marker='x', linestyle='', 
                color=cmap(i), markeredgecolor=cmap(i), markerfacecolor=cmap(i), 
                markersize=6, zorder=2)  # zorderを大きく設定

    ax.set_xlabel(r"$V_\mathrm{ds}\,$[V]")
    ax.set_ylabel(r"$I_\mathrm{d}\,$[A]")
    
    # カスタム凡例の作成
    legend_elements = [Line2D([0], [0], color='black', lw=2, label='Model'),
                      Line2D([0], [0], color='black', lw=2, linestyle='', 
                            marker='', markerfacecolor='none', markeredgecolor='black', label='Measurement')]
    
    # Vgsの値でソートした凡例要素を追加
    for i, vgs in enumerate(vgs_values):
        legend_elements.append(Line2D([0], [0], marker='x', color='w', 
                               label=f'Vgs={vgs}V', markerfacecolor=cmap(i), markeredgecolor=cmap(i), markersize=6))

    ax.legend(handles=legend_elements, loc='lower right', 
              title='', fontsize=20)
    
    plt.xlim(0,80)
    plt.ylim(0,25)
    # plt.tight_layout()
    plt.xticks(np.arange(0,90,10))
    plt.tick_params(axis='x', pad=10)  # x軸の数字の距離を10ポイントに設定
    plt.tick_params(axis='y', pad=15)  # y軸の数字の距離を15ポイントに設定
    # plt.savefig(os.path.join(base_dir, "IV_meas_vs_model.pdf"), bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    base_dir = r"H:\マイドライブ\nmashi\Sample_PCIM\data\Id-Vds"
    para_base_dir = r"H:\マイドライブ\nmashi\Sample_PCIM\data\Id-Vds"
    data = load_data(base_dir)
    params = load_parameters(para_base_dir+"\\"+"Id_results.txt")
    plot_iv_curve(data, base_dir, params)