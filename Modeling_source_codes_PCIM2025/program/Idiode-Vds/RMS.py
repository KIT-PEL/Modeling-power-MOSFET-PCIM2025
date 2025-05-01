import pandas as pd
import numpy as np

def compute_rms(df, start_time=0.4e-6, num_points=100):
    """計算指定されたtimeの直後のデータのRMS"""
    subset = df[df['time'] >= start_time].head(num_points)
    rms_vds = np.sqrt(np.mean(subset['Vds'] ** 2))
    rms_id = np.sqrt(np.mean(subset['Id'] ** 2))
    rms_vdd = np.sqrt(np.mean(subset['Vdd'] ** 2))
    rms_vgs_meas = np.sqrt(np.mean(subset['Vgs_meas'] ** 2))
    return rms_vds, rms_id, rms_vdd, rms_vgs_meas
