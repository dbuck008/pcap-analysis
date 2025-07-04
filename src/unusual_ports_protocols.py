import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_port_activity_trace(proto_df, port_df, top_n=10, title_suffix='', save=False, save_path='plots/port_protocol_activity/'):
    # --- Protocol Plot ---
    top_proto = proto_df.sort_values('event_pct', ascending=False).head(top_n)
    x = np.arange(len(top_proto))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - width/2, top_proto['baseline_pct'], width, label='Baseline')
    ax.bar(x + width/2, top_proto['event_pct'], width, label='Event')
    ax.set_xticks(x)
    ax.set_xticklabels(top_proto.index.astype(str), rotation=45, ha='right')
    ax.set_title(f'Top {top_n} Protocols: Baseline vs Event {title_suffix}')
    ax.set_ylabel('Traffic Share (%)')
    ax.legend()
    plt.tight_layout()
    
    if save:
        filename = f'{save_path}{f'Unusual Protocols - {title_suffix}'}.png'
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()

    # --- Port Plot ---
    top_ports = port_df.sort_values('event_pct', ascending=False).head(top_n)
    x = np.arange(len(top_ports))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - width/2, top_ports['baseline_pct'], width, label='Baseline')
    ax.bar(x + width/2, top_ports['event_pct'], width, label='Event')
    ax.set_xticks(x)
    ax.set_xticklabels(top_ports.index.astype(str), rotation=45, ha='right')
    ax.set_title(f'Top {top_n} Ports: Baseline vs Event {title_suffix}')
    ax.set_ylabel('Traffic Share (%)')
    ax.legend()
    plt.tight_layout()
    
    if save:
        filename = f'{save_path}{f'Unusual Ports - {title_suffix}'}.png'
        plt.savefig(filename)
        plt.close()
    else:
        plt.show()

def plot_port_protocol_activity(df_baseline, df_event, port='src', top_n=10, save=False, save_path='plots/port_protocol_activity/'):
    df_baseline = df_baseline.copy()
    df_event = df_event.copy()

    if save:
        os.makedirs(save_path, exist_ok=True)

    def count_values(df, port='src'):
        # Combine TCP and UDP ports
        if port=='dst':
            ports = pd.concat([
                df['tcp.dstport'].dropna().astype(int),
                df['udp.dstport'].dropna().astype(int)
            ])
        else:
            ports = pd.concat([
                df['tcp.srcport'].dropna().astype(int),
                df['udp.srcport'].dropna().astype(int)
            ])
        port_counts = ports.value_counts()

        proto_counts = df['ip.proto'].value_counts()
        return proto_counts, port_counts
    
    base_proto, base_ports = count_values(df_baseline, port)
    event_proto, event_ports = count_values(df_event, port)

    # Merge baseline + event counts
    proto_df = pd.DataFrame({'baseline': base_proto, 'event': event_proto}).fillna(0)
    proto_df['baseline_pct'] = proto_df['baseline']/proto_df['baseline'].sum() * 100
    proto_df['event_pct'] = proto_df['event']/proto_df['event'].sum() * 100

    port_df = pd.DataFrame({'baseline': base_ports, 'event': event_ports}).fillna(0)
    port_df['baseline_pct'] = port_df['baseline']/port_df['baseline'].sum() * 100
    port_df['event_pct'] = port_df['event']/port_df['event'].sum() * 100

    plot_port_activity_trace(proto_df, port_df, title_suffix=f'({port} ports)', top_n=top_n, save=save)


# def detect_anomolous_port_protocols(df_baseline, df_event, method='zscore', z_thresh=2.0, save=False, save_path='plots/unusual_ports_protocols/'):
#     # this isnt' working yet

#     df_baseline = df_baseline.copy()
#     df_event = df_event.copy()

#     if save:
#         os.makedirs(save_path, exist_ok=True)

#     def count_values(df):
#         # Combine TCP and UDP ports
#         ports = pd.concat([
#             df['tcp.dstport'].dropna().astype(int),
#             df['udp.dstport'].dropna().astype(int)
#         ])
#         port_counts = ports.value_counts()

#         proto_counts = df['ip.proto'].value_counts()
#         return proto_counts, port_counts
    
#     base_proto, base_ports = count_values(df_baseline)
#     event_proto, event_ports = count_values(df_event)

#     # Merge baseline + event counts
#     proto_df = pd.DataFrame({'baseline': base_proto, 'event': event_proto}).fillna(0)
#     proto_df['baseline_pct'] = proto_df['baseline']/proto_df['baseline'].sum() * 100
#     proto_df['event_pct'] = proto_df['event']/proto_df['event'].sum() * 100

#     port_df = pd.DataFrame({'baseline': base_ports, 'event': event_ports}).fillna(0)
#     port_df['baseline_pct'] = port_df['baseline']/port_df['baseline'].sum() * 100
#     port_df['event_pct'] = port_df['event']/port_df['event'].sum() * 100

#     plot_port_activity_trace(proto_df, port_df, top_n=10, save=save)


#     # Function to detect outliers using z-score
#     def flag_zscore(df):
#         mean = df['baseline_pct'].mean()
#         std = df['baseline_pct'].std()
#         df['zscore'] = (df['event_pct'] - mean).abs() / std
#         return df[df['zscore'] > z_thresh].sort_values('zscore', ascending=False)

#     # Function to detect outliers using IQR
#     def flag_iqr(df):
#         Q1 = df['baseline_pct'].quantile(0.25)
#         Q3 = df['baseline_pct'].quantile(0.75)
#         IQR = Q3 - Q1
#         threshold = Q3 + 1.5 * IQR
#         return df[(df['event_pct'] > threshold)].sort_values('event', ascending=False)

#     if method == 'zscore':
#         unusual_proto = flag_zscore(proto_df)
#         unusual_ports = flag_zscore(port_df)
#     elif method == 'iqr':
#         unusual_proto = flag_iqr(proto_df)
#         unusual_ports = flag_iqr(port_df)
#     else:
#         raise ValueError("Method must be 'zscore' or 'iqr'")

#     plot_port_activity_trace(unusual_proto, unusual_ports, top_n=10, title_suffix=f'(Z-Score > {z_thresh})', save=save)

