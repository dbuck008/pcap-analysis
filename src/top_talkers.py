import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def plot_top_talkers(df, top_n=10, save=False, save_path='plots/top_talkers/'):
    df = df.copy()
    
    if save:
        os.makedirs(save_path, exist_ok=True)

    # Total bytes sent per source
    grouped = df.groupby('ip.src')['frame.len'].sum().reset_index(name='bytes_sent')

    # Calculate total traffic
    total_bytes = grouped['bytes_sent'].sum()

    # Top N only
    top_talkers = grouped.sort_values(by='bytes_sent', ascending=False).head(top_n)

    # Add percentage of total
    top_talkers['traffic_pct'] = (top_talkers['bytes_sent'] / total_bytes) * 100
        
    ax = top_talkers.plot.bar(x='ip.src', y='traffic_pct', legend=False, figsize=(10, 5), color='skyblue')
    plt.ylabel('Traffic Share (%)')
    plt.xlabel('IP address')
    plt.title('Top Talkers (by % of Total Bytes Sent)')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 100)
    plt.tight_layout()
    
    if save:
        filename = f'{save_path}_{'Top Talkers (by % of Total Bytes Sent)'}.png'
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()


def compare_top_talkers(df_baseline, df_event, top_n=10, save=False, save_path='plots/top_talkers/'):
    df_baseline = df_baseline.copy()
    df_event = df_event.copy()
    
    if save:
        os.makedirs(save_path, exist_ok=True)

    # Total bytes for normalization
    total_baseline = df_baseline['frame.len'].sum()
    total_event = df_event['frame.len'].sum()

    # Group by source IP
    baseline_group = df_baseline.groupby('label')['frame.len'].sum().rename('baseline_bytes').reset_index()
    event_group = df_event.groupby('label')['frame.len'].sum().rename('event_bytes').reset_index()

    # Merge and calculate % of total
    merged = pd.merge(baseline_group, event_group, on='label', how='outer').fillna(0)
    merged['baseline_pct'] = (merged['baseline_bytes'] / total_baseline) * 100
    merged['event_pct'] = (merged['event_bytes'] / total_event) * 100

    # Sort by total traffic to get top N
    merged['total_bytes'] = merged['baseline_bytes'] + merged['event_bytes']
    top_talkers = merged.sort_values(by='total_bytes', ascending=False).head(top_n)

    x = np.arange(len(top_talkers))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width/2, top_talkers['baseline_pct'], width, label='Baseline')
    ax.bar(x + width/2, top_talkers['event_pct'], width, label='Event')

    ax.set_ylabel('Traffic Share (%)')
    plt.xlabel('Host')
    ax.set_title('Top Talkers: Baseline vs Event Traffic')
    ax.set_xticks(x)
    ax.set_xticklabels(top_talkers['label'], rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()

    if save:
        filename = f'{save_path}_{'Top Talkers (by % of Total Bytes Sent)'}.png'
        plt.savefig(filename)
    else:
        plt.show()

def plot_top_receivers(df, top_n=10, save=False, save_path='plots/top_receivers/'):
    df = df.copy()
    
    if save:
        os.makedirs(save_path, exist_ok=True)

    # Total bytes sent per source
    grouped = df.groupby('ip.dst')['frame.len'].sum().reset_index(name='bytes_received')

    # Calculate total traffic
    total_bytes = grouped['bytes_received'].sum()

    # Top N only
    top_receivers = grouped.sort_values(by='bytes_received', ascending=False).head(top_n)

    # Add percentage of total
    top_receivers['traffic_pct'] = (top_receivers['bytes_received'] / total_bytes) * 100
        
    ax = top_receivers.plot.bar(x='ip.dst', y='traffic_pct', legend=False, figsize=(10, 5), color='skyblue')
    plt.ylabel('Traffic Share (%)')
    plt.xlabel('IP address')
    plt.title('Top Receivers (by % of Total Bytes Sent)')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 100)
    plt.tight_layout()
    
    if save:
        filename = f'{save_path}_{'Top Receivers (by % of Total Bytes Sent)'}.png'
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()

def compare_top_receivers(df_baseline, df_event, top_n=10, save=False, save_path='plots/top_receivers/'):
    df_baseline = df_baseline.copy()
    df_event = df_event.copy()
    
    if save:
        os.makedirs(save_path, exist_ok=True)

    # Total bytes for normalization
    total_baseline = df_baseline['frame.len'].sum()
    total_event = df_event['frame.len'].sum()

    # Group by source IP
    baseline_group = df_baseline.groupby('ip.dst')['frame.len'].sum().rename('baseline_bytes').reset_index()
    event_group = df_event.groupby('ip.dst')['frame.len'].sum().rename('event_bytes').reset_index()

    # Merge and calculate % of total
    merged = pd.merge(baseline_group, event_group, on='ip.dst', how='outer').fillna(0)
    merged['baseline_pct'] = (merged['baseline_bytes'] / total_baseline) * 100
    merged['event_pct'] = (merged['event_bytes'] / total_event) * 100

    # Sort by total traffic to get top N
    merged['total_bytes'] = merged['baseline_bytes'] + merged['event_bytes']
    top_talkers = merged.sort_values(by='total_bytes', ascending=False).head(top_n)

    x = np.arange(len(top_talkers))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width/2, top_talkers['baseline_pct'], width, label='Baseline')
    ax.bar(x + width/2, top_talkers['event_pct'], width, label='Event')

    ax.set_ylabel('Traffic Share (%)')
    plt.xlabel('Host')
    ax.set_title('Top Receivers: Baseline vs Event Traffic')
    ax.set_xticks(x)
    ax.set_xticklabels(top_talkers['ip.dst'], rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()

    if save:
        filename = f'{save_path}_{'Top Receivers (by % of Total Bytes Sent)'}.png'
        plt.savefig(filename)
    else:
        plt.show()
