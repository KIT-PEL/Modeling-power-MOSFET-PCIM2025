import os
import pandas as pd

def load_data(base_dir):
    # Vgsの範囲を指定
    vgs_list = ["0.00"]
    
    data = {}
    
    for vgs in vgs_list:
        vgs_dir = os.path.join(base_dir, f"Vgs={vgs}")
        vdd_data = {}
        
        # VddごとのCSVファイルを読み込む
        for filename in os.listdir(vgs_dir):
            if filename.endswith("_ALL.csv"):
                vdd_value = filename.split('=')[1].split('_')[0]
                file_path = os.path.join(vgs_dir, filename)
                df = pd.read_csv(file_path, skiprows=16, header=None, names=["time", "Vds", "Vdd", "Vgs_meas", "Id"])
                vdd_data[vdd_value] = df
                
        data[vgs] = vdd_data

    return data
