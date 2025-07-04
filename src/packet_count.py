import pandas as pd #sudo apt install python3-pandas
import matplotlib.pyplot as plt
import os
from src.annotate_graph import *

def plot_packet_count_trace(df, title, x_label='Time', y_label='Mbps', save=False, save_path=None, events=None):
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df['frame.time_epoch'], df['packet_count'])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.tight_layout()

    add_events_to_graph(ax, events)

    if save:
        filename = f'{save_path}{title.replace("\n","-")}.png'
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()

def plot_packet_count(data, graphs='overall', interval='1Min', save=False, save_path='plots/packet_count/', events=None, rolling_window=None):
    """
    Plot packets/interval graph for each VLAN (and protocol) combination.

    Args:
        data (pd.DataFrame | list[baseline_df, event_df] of df (pd.DataFrame): DataFrame with 'frame.time_epoch', 'frame.len', 'vlan.id', and 'ip.proto'
        graphs (str | list[string]): Choose which graphs to plot (e.g. 'overall', 'vlan', 'protocol')
        interval (str): Resample interval (e.g., '1S', '1Min', '10Min')
        save (bool): If True, saves plots as PNGs
        save_path (str): Path to save plots
        events (pd.DataFrame): DataFrame containing the events to highlight on the graphs
    """

    if save:
        os.makedirs(save_path, exist_ok=True)

    # determine if data is one DataFrame or two
    if isinstance(data, list) and len(data) == 2:
        baseline, event = data
        names= ['Baseline', 'Event']
    elif isinstance(data, pd.DataFrame):
        data = [data]
        names = ['Data']
    else:
        raise ValueError("First arg must be a DataFrame, or list containing two DataFrames")
    
    for x in range(len(data)):
        df = data[x].copy()

        # Group and count packets
        grouped = df.groupby(['vlan.id', 'protocol', pd.Grouper(key='frame.time_epoch', freq=interval)]).size().reset_index(name='packet_count')
        
        # apply rolling window
        if rolling_window:
            grouped['packet_count'] = grouped.groupby(['vlan.id', 'protocol'])['packet_count'].transform(lambda x: x.rolling(window=rolling_window, min_periods=1).mean())

        if 'overall' in graphs:
            pivot = grouped.pivot_table(index='frame.time_epoch', columns='vlan.id', values='packet_count').fillna(0)

            # Plot
            ax = pivot.plot(figsize=(14, 6), title=f'Total Packets per VLAN\n({names[x]} - All Protocols - {interval})')
            plt.xlabel('Time')
            plt.ylabel('Packets')
            plt.legend(title='VLAN ID')
            plt.tight_layout()

            add_events_to_graph(ax, events)
            if save:
                plt.savefig(f'{save_path}Total Packets per VLAN ({names[x]} - All Protocols - {interval}).png')
                plt.close()
            else:
                plt.show()
        if 'vlan' in graphs:
            # Get unique VLANs
            vlan_ids = grouped['vlan.id'].unique()

            for vlan in vlan_ids:
                vlan_df = grouped[grouped['vlan.id'] == vlan]
                plot_packet_count_trace(vlan_df, f'Packet count for VLAN {vlan}\n({names[x]} - {interval} intervals)', save=save, save_path=save_path, events=events)
        if 'protocol' in graphs:
            # Plot each VLAN + protocol combination
            for (vlan, protocol), vlan_proto_df in grouped.groupby(['vlan.id', 'protocol']):
                plot_packet_count_trace(vlan_proto_df, f'Packet count for VLAN {vlan} - {protocol}\n({names[x]} - {interval} intervals)', save=save, save_path=save_path, events=events)