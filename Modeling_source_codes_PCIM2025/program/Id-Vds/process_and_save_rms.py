import os
import pandas as pd
from data_loader import load_data
from RMS import compute_rms

def process_data(base_dir, output_file):
    """
    データフレームを読み込み、フォーマットを変形しcsvを出力
    """
    # データの読み込み
    data = load_data(base_dir)
    # 結果を格納するリスト
    results = []

    # データを処理
    for vgs, vdd_data in data.items():
        for vdd, df in vdd_data.items():
            rms_vds, rms_id, rms_vdd, rms_vgs_meas = compute_rms(df)
            results.append([vgs, rms_vds, rms_id, rms_vdd, rms_vgs_meas])

    # DataFrameに変換
    df_results = pd.DataFrame(results, columns=["Vgs", "Vds(RMS)", "Id(RMS)", "Vdd(RMS)", "Vgs_meas(RMS)"])
    
    # CSVファイルに保存
    df_results.to_csv(os.path.join(base_dir,output_file), index=False, header=False)

if __name__ == "__main__":
    base_dir = r"H:\マイドライブ\nmashi\Sample_PCIM\data\Id-Vds"
    output_file = "rms_results.csv"
    process_data(base_dir, output_file)
