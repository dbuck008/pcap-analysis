import pandas as pd #sudo apt install python3-pandas
import matplotlib.pyplot as plt
import os
import plotly.tools as tls
import plotly.offline as py
import plotly.graph_objs as go
import src.my_plot as my_plot


def plot_bandwidth(df, graphs='overall', result='png', interval='1Min', save=False, save_path='plots/bandwidth/', events=None, rolling_window=None):
    """
    Plot a bandwidth graph for each VLAN (and protocol) combination.

    Args:
        data (pd.DataFrame | list[baseline_df, event_df] of df (pd.DataFrame): DataFrame with 'frame.time_epoch', 'frame.len', 'vlan.id', and 'ip.proto'
        graphs (str | list[string]): Choose which graphs to plot (e.g. 'overall', 'vlan', 'protocol')
        interval (str): Resample interval (e.g., '1S', '1Min', '10Min')
        save (bool): If True, saves plots as PNGs
        save_path (str): Path to save plots
        events (pd.DataFrame): DataFrame containing the events to highlight on the graphs
        rolling_window (int): Optional rolling average window size (in intervals)
    """

    if save:
        os.makedirs(save_path, exist_ok=True)

    
    # Group and convert to Mbps
    grouped = df.groupby(['vlan.id', 'protocol', pd.Grouper(key='frame.time_epoch', freq=interval)])['frame.len'].sum().reset_index()
    grouped['bandwidth'] = (grouped['frame.len'] * 8) / (pd.to_timedelta(interval).total_seconds() * 10**6)
    
    # apply rolling window
    if rolling_window:
        grouped['bandwidth'] = grouped.groupby(['vlan.id', 'protocol'])['bandwidth'].transform(lambda x: x.rolling(window=rolling_window, min_periods=1).mean())

    date = df['frame.time_epoch'].iloc[0].strftime("%d %b %Y")
    if 'overall' in graphs:
        # plots one graph showing andwidth on each vlan where each vlan is a different line on the graph
        pivot = grouped.pivot_table(index='frame.time_epoch', columns='vlan.id', values='bandwidth', aggfunc='sum').fillna(0)

        my_plot.plot_pivot(pivot,
                            title=f'Bandwidth per VLAN - ({interval} interval)',
                            x_label='Time (Zulu)',
                            y_label='Bandwidth (Mbps)',
                            result=result,
                            save_path=save_path,
                            events=events)

    if 'vlan' in graphs:
        # plot one graph per vlan

        # Get unique VLANs
        vlan_ids = grouped['vlan.id'].unique()

        for vlan in vlan_ids:
            vlan_df = grouped[grouped['vlan.id'] == vlan].groupby('frame.time_epoch')['bandwidth'].sum().reset_index()
            my_plot.plot_line(x=vlan_df['frame.time_epoch'], 
                                y=vlan_df['bandwidth'],
                                title=f'Bandwidth for VLAN {vlan} -({interval} interval)',
                                x_label='Time (Zulu)',
                                y_label='Bandwidth (Mbps)',
                                result=result,
                                save_path=save_path,
                                events=events
            )
    if 'protocol' in graphs:
        # plot on graph per vlan, per protocol

        # Plot each VLAN + protocol combination
        for (vlan, protocol), vlan_proto_df in grouped.groupby(['vlan.id', 'protocol']):
            my_plot.plot_line(x=vlan_proto_df['frame.time_epoch'], 
                                y=vlan_proto_df['bandwidth'],
                                title=f'Bandwidth for VLAN {vlan} - {protocol} - ({interval} interval)',
                                x_label='Time (Zulu)',
                                y_label='Bandwidth (Mbps)',
                                result=result,
                                save_path=save_path,
                                events=events
            )
        
