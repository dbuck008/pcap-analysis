
import pandas as pd
import matplotlib.pyplot as plt
import os 

def plot_jitter(df, interval='1Min', save=False, save_path='plots/jitter/'):
    # this isn't working properly. It's measuring jitter between [ip.src, ip,dst, vlan.id] packets - not all outobund packets on a vlan
    # I could measure jitter on a vlan, but that doesn't consider bi-directional traffic
    # can I measure jitter between packets from the same subnet?
    # example subnet filtering: df['ip.src'].apply(lambda x: x[0:6]=='10.0.1')

    
    df = df.copy()

    if save:
        os.makedirs(save_path, exist_ok=True)

    # Sort and calculate inter-arrival deltas
    df = df.sort_values(['ip.src', 'ip.dst', 'vlan.id', 'frame.time_epoch'])
    df['time_diff'] = df.groupby(['ip.src', 'ip.dst', 'vlan.id'])['frame.time_epoch'].diff().dt.total_seconds()
    df['jitter'] = df.groupby(['ip.src', 'ip.dst', 'vlan.id'])['time_diff'].diff().abs()

    # Resample jitter per VLAN over time
    df['time_bin'] = df['frame.time_epoch'].dt.floor(interval)
    jitter_over_time = df.groupby(['vlan.id', 'time_bin'])['jitter'].mean().reset_index()

    # Plot
    for vlan in jitter_over_time['vlan.id'].unique():
        vlan_data = jitter_over_time[jitter_over_time['vlan.id'] == vlan]
        plt.figure(figsize=(12, 4))
        plt.plot(vlan_data['time_bin'], vlan_data['jitter'], marker='o')
        plt.title(f'Jitter Over Time for VLAN {vlan}')
        plt.xlabel('Time')
        plt.ylabel('Average Jitter (seconds)')
        plt.grid(True)
        plt.tight_layout()
        if save:
            filename = f'{save_path}Jitter Over Time for VLAN {vlan}.png'
            plt.savefig(filename)
            plt.close()
        else:
            plt.show()

