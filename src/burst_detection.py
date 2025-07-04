
import os
import pandas as pd
import matplotlib.pyplot as plt

def detect_bandwidth_bursts(df, interval='1Min', z_thresh=2.5, rolling_window=10, plot=True, save=False, save_path="plots/burst/"):
    if save:
        os.makedirs(save_path, exist_ok=True)

    df = df.copy()
    
    # Group by interval and VLAN
    df['time_bin'] = df['frame.time_epoch'].dt.floor(interval)
    traffic = df.groupby(['vlan.id', 'time_bin'])['frame.len'].sum().reset_index()
    traffic['bandwidth_mbps'] = (traffic['frame.len'] * 8) / (pd.to_timedelta(interval).total_seconds() * 10**6)

    for vlan in traffic['vlan.id'].unique():
        vlan_data = traffic[traffic['vlan.id'] == vlan].copy()
        vlan_data['rolling_avg'] = vlan_data['bandwidth_mbps'].rolling(rolling_window, min_periods=1).mean()
        vlan_data['rolling_std'] = vlan_data['bandwidth_mbps'].rolling(rolling_window, min_periods=1).std()
        vlan_data['zscore'] = (vlan_data['bandwidth_mbps'] - vlan_data['rolling_avg']) / vlan_data['rolling_std']
        vlan_data['is_burst'] = (vlan_data['zscore'] > z_thresh) | (vlan_data['zscore'] < -1*z_thresh)

        if plot:
            plt.figure(figsize=(12, 4))
            plt.plot(vlan_data['time_bin'], vlan_data['bandwidth_mbps'], label='Bandwidth (Mbps)')
            plt.scatter(vlan_data[vlan_data['is_burst']]['time_bin'],
                        vlan_data[vlan_data['is_burst']]['bandwidth_mbps'],
                        color='red', label='Burst', zorder=5)
            plt.title(f'Bandwidth and Bursts for VLAN {vlan}\nZ-threshold = {z_thresh}')
            plt.xlabel('Time')
            plt.ylabel('Bandwidth (Mbps)')
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            if save:
                plt.savefig(f'{save_path}Bandwidth and Bursts for VLAN {vlan}.png')
                plt.close()
            else:
                plt.show()
