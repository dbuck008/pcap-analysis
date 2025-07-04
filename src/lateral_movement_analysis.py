
import os
import pandas as pd
import matplotlib.pyplot as plt

def lateral_movement_analysis(event_traffic, baseline_traffic=None, interval='10Min', save=False, save_path='plots/lateral/'):
    if save:
        os.makedirs(save_path, exist_ok=True)

    event_traffic = event_traffic.copy()
    
    event_traffic['time_bin'] = event_traffic['frame.time_epoch'].dt.floor(interval)

    # 1. Fan-out analysis
    fanout = event_traffic.groupby(['time_bin', 'ip.src'])['ip.dst'].nunique().reset_index()
    fanout.rename(columns={'ip.dst': 'unique_dsts'}, inplace=True)

    # Flag sources with high fan-out (e.g., 90th percentile)
    threshold = fanout['unique_dsts'].quantile(0.90)
    fanout['fanout_alert'] = fanout['unique_dsts'] > threshold

    # 2. Port-target mapping (per source)
    port_target_mapping = event_traffic.copy()
    port_target_mapping['dst_port'] = port_target_mapping['tcp.dstport'].fillna(port_target_mapping['udp.dstport'])

    # Count how many distinct IPs each source hits per port
    port_targets = port_target_mapping.groupby(['ip.src', 'dst_port'])['ip.dst'].nunique().reset_index()
    port_targets.rename(columns={'ip.dst': 'num_targets'}, inplace=True)

    # Flag if a port is used across many targets (e.g., 5+)
    port_targets['portspread_alert'] = port_targets['num_targets'] > 5 # todo: change this value based on data?

    # 3. New peer detection
    new_peers = pd.DataFrame()
    if baseline_traffic is not None:
        baseline_traffic['peer'] = baseline_traffic['ip.src'] + '->' + baseline_traffic['ip.dst']
        event_traffic['peer'] = event_traffic['ip.src'] + '->' + event_traffic['ip.dst']
        known_peers = set(baseline_traffic['peer'].unique())
        event_traffic['new_peer'] = ~event_traffic['peer'].isin(known_peers)
        new_peers = event_traffic[event_traffic['new_peer']].groupby('ip.src')['ip.dst'].nunique().reset_index()
        new_peers.rename(columns={'ip.dst': 'new_unique_dsts'}, inplace=True)

    for ip in fanout['ip.src'].unique():
        ip_data = fanout[fanout['ip.src'] == ip]
        if ip_data['fanout_alert'].any():
            plt.figure(figsize=(12, 4))
            plt.plot(ip_data['time_bin'], ip_data['unique_dsts'], label='Unique Destinations')
            plt.axhline(y=threshold, color='red', linestyle='--', label='Fan-Out Threshold')
            plt.title(f'Fan-Out Over Time for {ip}')
            plt.xlabel('Time')
            plt.ylabel('# Unique Destinations')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            if save:
                plt.savefig(f'{save_path}Fan-Out Over Time for {ip}).png')
                plt.close()
            else:
                plt.show()

    return {
        'fanout_alerts': fanout[fanout['fanout_alert']],
        'portscan_alerts': portscan_summary[portscan_summary['portscan_alert']],
        'new_peer_alerts': new_peers if not new_peers.empty else None
    }
