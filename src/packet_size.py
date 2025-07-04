import pandas as pd
import matplotlib.pyplot as plt
import os
from src.annotate_graph import *

def plot_avg_packet_size(df, title, x_label='Time', y_label='Avg Packet Size (Bytes)', save=False, save_path=None, events=None):
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df['frame.time_epoch'], df['avg_packet_size'])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.tight_layout()
    add_events_to_graph(ax, events)

    if save:
        filename = f"{save_path}{title.replace('\n', '-')}.png"
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()


def plot_avg_packet_sizes(data, graphs='overall', interval='1Min', save=False, save_path='plots/avg_packet_size/', events=None, rolling_window=None):
    """
    Plot average packet size (bytes) per time interval.

    Args:
        df (pd.DataFrame): DataFrame with 'frame.time_epoch', 'frame.len', 'vlan.id', and 'ip.proto'
        graphs (str): 'overall', 'vlan', or 'protocol'
        interval (str): Time bucket size
        save (bool): Save PNGs
        save_path (str): Directory to save plots
        events (pd.DataFrame): Optional DataFrame of events
        rolling_window (int): Window size for smoothing
    """

    if save:
        os.makedirs(save_path, exist_ok=True)

    # determine if data is one DataFrame or two
    if isinstance(data, list) and len(data) == 2:
        names= ['Baseline', 'Event']
    elif isinstance(data, pd.DataFrame):
        data = [data]
        names = ['Data']
    else:
        raise ValueError("First arg must be a DataFrame, or list containing two DataFrames")
    
    for x in range(len(data)):
        df = data[x].copy()

        # Compute total bytes and count of packets
        bytes_grouped = df.groupby(['vlan.id', 'ip.proto', pd.Grouper(key='frame.time_epoch', freq=interval)])['frame.len'].sum().reset_index(name='total_bytes')
        count_grouped = df.groupby(['vlan.id', 'ip.proto', pd.Grouper(key='frame.time_epoch', freq=interval)]).size().reset_index(name='packet_count')

        # Merge and calculate average
        merged = pd.merge(bytes_grouped, count_grouped, on=['vlan.id', 'ip.proto', 'frame.time_epoch'])
        merged['avg_packet_size'] = merged['total_bytes'] / merged['packet_count']

        # Apply smoothing
        if rolling_window:
            merged['avg_packet_size'] = merged.groupby(['vlan.id', 'ip.proto'])['avg_packet_size'].transform(
                lambda x: x.rolling(window=rolling_window, min_periods=1).mean()
            )

        if 'overall' in graphs:
            pivot = merged.pivot_table(index='frame.time_epoch', columns='vlan.id', values='avg_packet_size').fillna(0)
            ax = pivot.plot(figsize=(12, 4), title=f'Average Packet Size per VLAN\n({names[x]} - {interval})')
            plt.xlabel('Time')
            plt.ylabel('Avg Packet Size (Bytes)')
            plt.legend(title='VLAN ID')
            plt.tight_layout()
            add_events_to_graph(ax, events)

            if save:
                plt.savefig(f"{save_path}Average Packet Size for VLAN - ({names[x]} - {interval}).png")
                plt.close()
            else:
                plt.show()

        if 'vlan' in graphs:
            for vlan in merged['vlan.id'].unique():
                vlan_df = merged[merged['vlan.id'] == vlan]
                plot_avg_packet_size(vlan_df, f'Average Packet Size for VLAN {vlan}\n({names[x]} - {interval})', save=save, save_path=save_path, events=events)

        if 'protocol' in graphs:
            for (vlan, proto), vlan_proto_df in merged.groupby(['vlan.id', 'ip.proto']):
                plot_avg_packet_size(vlan_proto_df, f'Avg Packet Size for VLAN {vlan} - Protocol {proto}\n({names[x]} - {interval})', save=save, save_path=save_path, events=events)
