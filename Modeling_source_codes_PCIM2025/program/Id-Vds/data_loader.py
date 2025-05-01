import os
import pandas as pd

def load_data(base_dir):
    """
    Edit:
        match vgs_list and file name format
    Return:
        dataframe
    """
    # Vgs range
    vgs_list = ["4.00", "6.00", "8.00", "10.00", "12.00", "14.00","16.00","18.00","20.00"]
    
    data = {}
    
    for vgs in vgs_list:
        print("Vgs =",vgs,"のデータを読み込み中")
        vgs_dir = os.path.join(base_dir, f"Vgs={vgs}")
        vdd_data = {}
        
        # read csv files seperately for each Vdd
        for filename in os.listdir(vgs_dir):
            if filename.endswith("_ALL.csv"):
                vdd_value = filename.split('=')[1].split('_')[0]
                file_path = os.path.join(vgs_dir, filename)
                df = pd.read_csv(file_path, skiprows=16, header=None, names=["time", "Vds", "Vdd", "Vgs_meas", "Id"])
                vdd_data[vdd_value] = df
                
        data[vgs] = vdd_data

    print("データ読み込み完了 - Data read complete")
    return data
