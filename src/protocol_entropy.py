import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def calculate_protocol_entropy(df, interval='5Min', save=False, save_path='plots/entropy/'):
    
    if save:
        os.makedirs(save_path, exist_ok=True)
    
    df = df.copy()

    df['time_bin'] = df['frame.time_epoch'].dt.floor(interval)

    entropy_records = []

    for (vlan, time), group in df.groupby(['vlan.id', 'time_bin']):
        proto_counts = group['ip.proto'].value_counts(normalize=True)
        entropy = -np.sum(proto_counts * np.log2(proto_counts))
        entropy_records.append({'vlan.id': vlan, 'time_bin': time, 'entropy': entropy})

    entropy_df = pd.DataFrame(entropy_records)

    for vlan in entropy_df['vlan.id'].unique():
        vlan_data = entropy_df[entropy_df['vlan.id'] == vlan]
        plt.figure(figsize=(12, 4))
        plt.plot(vlan_data['time_bin'], vlan_data['entropy'], marker='o')
        plt.title(f'Protocol Entropy Over Time for VLAN {vlan}')
        plt.xlabel('Time')
        plt.ylabel('Entropy (bits)')
        plt.grid(True)
        plt.tight_layout()
        if save:
            plt.savefig(f'{save_path}Protocol Entropy Over Time for VLAN {vlan}.png')
            plt.close()
        else:
            plt.show()
