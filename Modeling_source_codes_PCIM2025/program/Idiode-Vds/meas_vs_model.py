import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from data_loader import load_data
from RMS import compute_rms

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
    params = {}
    with open(filename, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=')
                params[key.strip()] = float(value.strip())
    return params

def calculate_id(Vds, Vgs, params):
    # モデルパラメータ
    IS = params["IS"]
    RD = params["RD"]
    KB = params["KB"]

    # 初期化
    gmin = 1e-12
    rmin = 0.0
    rmax = 1.0

    # Vds が配列の場合に対応するための処理
    if np.any(Vds < 0.0):
        Vds = np.maximum(Vds, 0.0)  # Vdsが0未満の場合は0に修正

    # バイナリサーチを用いて Id を計算
    Ids_list = []
    for vds in Vds:  # 各Vdsに対して計算を行う
        rmin_local = rmin
        rmax_local = rmax

        for i in range(30):
            rtmp = (rmin_local + rmax_local) / 2.0
            Vdr = rtmp * vds

            if Vdr<0.0:
                Vdr=0.0

            Ids = IS * (np.exp(Vdr / RD) - 1.0)
            Id = Ids + gmin * vds

            # バイナリサーチによる収束判定
            if Id > (1.0 - rtmp) * vds / KB:
                rmax_local = rtmp
            elif Id < (1.0 - rtmp) * vds / KB:
                rmin_local = rtmp
            else:
                break

        Ids_list.append(Id)

    return np.array(Ids_list)  # 配列として返す


def plot_iv_curve(data, base_dir, params):
    fig, ax = plt.subplots()
    cmap = plt.get_cmap('tab10')
    vgs_values = sorted(data.keys())
    vgs_colors = {vgs: cmap(i) for i, vgs in enumerate(vgs_values)}
    # 理論モデルのプロット
    Vds = np.linspace(0, 100, 1000)
    for vgs in vgs_values:
        Id = calculate_id(Vds, vgs, params)
        ax.plot(Vds, Id, linestyle='-', color="black", label=f'Model')
    # 実験データのプロット
    for vgs, vdd_dict in data.items():
        rms_vds_list = []
        rms_id_list = []
        for vdd, df in vdd_dict.items():
            rms_vds, rms_id, _, _ = compute_rms(df)
            rms_vds_list.append(rms_vds)
            rms_id_list.append(rms_id)
        
        ax.plot(rms_vds_list, rms_id_list, marker='x', linestyle='', 
                color="tab:blue", label=f'Measurement', 
                markeredgecolor="tab:blue", markerfacecolor='none', markersize=6)

    

    ax.set_xlabel(r"$-V_\mathrm{ds}\,$[V]")
    ax.set_ylabel(r"$I_\mathrm{diode}\,$[A]")
    ax.legend(loc='upper left',fontsize=25)
    
    # plt.tight_layout(rect=[0, 0, 0.95, 1])
    plt.xlim(0,6)
    plt.ylim(0,15)
    plt.xticks(np.arange(0,7,1))
    # plt.tight_layout()
    plt.tick_params(axis='x', pad=10)  # x軸の数字の距離を10ポイントに設定
    plt.tick_params(axis='y', pad=15)  # y軸の数字の距離を15ポイントに設定
    plt.savefig(os.path.join(base_dir, "Idiode_meas_vs_model.pdf"), bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    base_dir = r"H:\マイドライブ\nmashi\Sample_PCIM\data\Idiode-Vds"
    data = load_data(base_dir)
    params = load_parameters(os.path.join(base_dir, "Idiode_results.txt"))
    plot_iv_curve(data, base_dir, params)