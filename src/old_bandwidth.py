import pandas as pd #sudo apt install python3-pandas
import matplotlib.pyplot as plt
import os
from src.annotate_graph import *

def plot_bandwidth_trace(df, title, x_label='Time', y_label='Mbps', save=False, save_path=None, events=None):
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df['frame.time_epoch'], df['bandwidth_mbps'])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.tight_layout()

    add_events_to_graph(ax, events)

    if save:
        filename = f'{save_path}_{title}.png'
        plt.savefig(filename)
    else:
        plt.show()

def plot_bandwidth(data, graphs='overall', interval='1Min', save=False, save_path='plots/bandwidth/', events=None, rolling_window=None):
    """
    Plot separate bandwidth graphs for each VLAN and protocol combination over the given interval.

    Args:
        df (pd.DataFrame): DataFrame with 'frame.time_epoch', 'frame.len', 'vlan.id', and 'ip.proto'
        type (str): Choose which graph to plot (e.g. 'overall', 'vlan', 'protocol')
        interval (str): Resample interval (e.g., '1S', '1Min', '10Min')
        save (bool): If True, saves plots as PNGs
        save_path (str): Path to save plots
        events (pd.DataFrame): DataFrame containing the events to highlight on the graphs
        rolling_window (int): Optional rolling average window size (in intervals)
    """

    if save:
        os.makedirs(save_path, exist_ok=True)

    data = data.copy()

    # Group and convert to Mbps
    grouped = data.groupby(['vlan.id', 'protocol', pd.Grouper(key='frame.time_epoch', freq=interval)])['frame.len'].sum().reset_index()
    grouped['bandwidth_mbps'] = (grouped['frame.len'] * 8) / (pd.to_timedelta(interval).total_seconds() * 10**6)
    
    # apply rolling window
    if rolling_window:
        grouped['bandwidth_mbps'] = grouped.groupby(['vlan.id', 'protocol'])['bandwidth_mbps'].transform(lambda x: x.rolling(window=rolling_window, min_periods=1).mean())

    if graphs == 'overall':
        pivot = grouped.pivot_table(index='frame.time_epoch', columns='vlan.id', values='bandwidth_mbps').fillna(0)

        # Plot
        ax = pivot.plot(figsize=(14, 6), title=f'Total Bandwidth per VLAN (All Protocols - {interval})')
        plt.xlabel('Time')
        plt.ylabel('Mbps')
        plt.legend(title='VLAN ID')
        plt.tight_layout()

        add_events_to_graph(ax, events)
        if save:
            plt.savefig(f'{save_path}Total Bandwidth per VLAN (All Protocols - {interval}).png')
            plt.close()
        else:
            plt.show()
    elif graphs == 'vlan':
        # Get unique VLANs
        vlan_ids = grouped['vlan.id'].unique()

        for vlan in vlan_ids:
            vlan_df = grouped[grouped['vlan.id'] == vlan]
            plot_bandwidth_trace(vlan_df, f'Bandwidth for VLAN {vlan} ({interval} intervals)', save=save, save_path=save_path, events=events)
    elif graphs == 'protocol':
        # Plot each VLAN + protocol combination
        for (vlan, protocol), vlan_proto_df in grouped.groupby(['vlan.id', 'protocol']):
            plot_bandwidth_trace(vlan_proto_df, f'Bandwidth for VLAN {vlan} - {protocol} ({interval} intervals)', save=save, save_path=save_path, events=events)
    else:
        print('Specify which graph you want to plot')
