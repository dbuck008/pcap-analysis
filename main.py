import subprocess
from src.read_events import *
from src.pcap_to_pandas import *
from src.bandwidth import * 
from src.top_talkers import *
from src.read_hostnames import *
from src.packet_count import *
from src.packet_size import *
from src.unusual_ports_protocols import *
from src.new_rare_conversations import *
from src.plot_jitter_over_time import *
from src.burst_detection import *
from src.protocol_entropy import *
from src.lateral_movement_analysis import *

def analyze(event_traffic_csv=None, baseline_traffic_csv=None, event_file=None, hostname_file=None, interval='1S', vlan_filter=None, protocol_filter=None, time_filter=None):
    
    if not event_traffic_csv and not baseline_traffic_csv:
        print("Can't analyze stuff if there's no capture file")
        return
    
    ### read the csv
    if event_traffic_csv: event_traffic = read_pcap_csv(event_traffic_csv)
    if baseline_traffic_csv: baseline_traffic = read_pcap_csv(baseline_traffic_csv)

    ### read the optional files
    event_log = read_events(event_file) if event_file else None
    hostnames = load_ip_hostname_mapping(hostname_file) if hostname_file else None
    
    ### clean up the data

    # Ensure timestamp and length are correct types
    if event_traffic_csv: event_traffic['frame.len'] = event_traffic['frame.len'].astype(int)
    if baseline_traffic_csv: baseline_traffic['frame.len'] = baseline_traffic['frame.len'].astype(int)
    
    # ensure vlan.id is an int
    # todo: need to check for NaN and insert something (maybe 0?)
    if event_traffic_csv: event_traffic['vlan.id'] = event_traffic['vlan.id'].astype(int)
    if baseline_traffic_csv: baseline_traffic['vlan.id'] = baseline_traffic['vlan.id'].astype(int)

    # Define protocol names
    protocol_map = {6: 'TCP', 17: 'UDP', 1: 'ICMP'} #todo: add more protocols here
    if event_traffic_csv: event_traffic['protocol'] = event_traffic['ip.proto'].map(protocol_map).fillna(event_traffic['ip.proto'].astype(str))
    if baseline_traffic_csv: baseline_traffic['protocol'] = baseline_traffic['ip.proto'].map(protocol_map).fillna(baseline_traffic['ip.proto'].astype(str))

    # map the ip addresss to text labels based on hostname_file
    if hostname_file:
        if event_traffic_csv: event_traffic['hostname'] = event_traffic['ip.src'].map(hostnames)
        if event_traffic_csv: event_traffic['label'] = event_traffic['hostname'].fillna(event_traffic['ip.src'])
        if baseline_traffic_csv: baseline_traffic['hostname'] = baseline_traffic['ip.src'].map(hostnames)
        if baseline_traffic_csv: baseline_traffic['label'] = baseline_traffic['hostname'].fillna(baseline_traffic['ip.src'])
    else:
        if event_traffic_csv: event_traffic['label'] = event_traffic['ip.src']
        if baseline_traffic_csv: baseline_traffic['label'] = baseline_traffic['ip.src']

    ### limit the data based on filters
    if vlan_filter is not None:
        if event_traffic_csv: event_traffic = event_traffic[event_traffic['vlan.id'].isin(vlan_filter)]
        if baseline_traffic_csv :baseline_traffic = baseline_traffic[baseline_traffic['vlan.id'].isin(vlan_filter)]

    if protocol_filter is not None:
        if event_traffic_csv: event_traffic = event_traffic[event_traffic['ip.proto'].isin(protocol_filter)]
        if baseline_traffic_csv: baseline_traffic = baseline_traffic[baseline_traffic['ip.proto'].isin(protocol_filter)]

    if time_filter is not None:
        start_time = pd.to_datetime(time_filter[0], unit='s')
        end_time = pd.to_datetime(time_filter[1], unit='s')
        if event_traffic_csv: event_traffic = event_traffic[(event_traffic['frame.time_epoch'] >= start_time) & (event_traffic['frame.time_epoch'] <= end_time)]
        if baseline_traffic_csv: baseline_traffic = baseline_traffic[(baseline_traffic['frame.time_epoch'] >= start_time) & (baseline_traffic['frame.time_epoch'] <= end_time)]
    
    
    ### Analyze

    # # Bandwidth
    plot_bandwidth(event_traffic, graphs=['overall', 'vlan', 'protocol'], result='html', save=True, events=event_log)

    # burst detection
    detect_bandwidth_bursts(event_traffic, save=True)

    # # # packet rate
    # plot_packet_count(event_traffic, graphs=['overall', 'vlan', 'protocol'], save=True, events=event_log)

    # # # average packet size 
    # plot_avg_packet_sizes(event_traffic, graphs=['overall', 'vlan', 'protocol'], save=True, events=event_log)

    # # # top talkers
    # # plot_top_talkers(event_traffic, save=True)
    # compare_top_talkers(baseline_traffic, event_traffic, save=True)

    # # Top receivers
    # # plot_top_receivers(event_traffic, save=True)
    # compare_top_receivers(baseline_traffic, event_traffic, save=True)


    # # # port and protocol activity
    # plot_port_protocol_activity(baseline_traffic, event_traffic, port='src', top_n=10, save=True)
    # plot_port_protocol_activity(baseline_traffic, event_traffic, port='dst', top_n=10, save=True)

    # # protocol entropy
    # calculate_protocol_entropy(event_traffic, save=True)

    # # jitter
    # plot_jitter(event_traffic, interval='1Min', save=True)

    # # new or rare converstaions
    # rare_flows = detect_new_or_rare_conversations(baseline_traffic, event_traffic, rare_threshold=3)
    # rare_flows.to_csv('rare_connections.csv', index=False)
    # print(rare_flows[['ip.src', 'ip.dst', 'ip.proto', 'count_baseline', 'count_event', 'is_new', 'is_rare']])

    # # latency

    # # lateral movement
    # lateral_movement_analysis(event_traffic, baseline_traffic, save=True)

    print("done")


# print("converting pcap to csv...")
# input_file = "pcaps/single/f5-honeypot-release.pcap"
# output_file = "files/event_traffic.csv"
# subprocess.run(["./pcap_to_csv.sh", input_file, output_file], capture_output=False, text=True)
# print("done coverting to csv")

event_traffic_csv='files/synthetic_network_model_pcap_strict.csv'
baseline_traffic_csv='files/synthetic_event_data.csv'
event_file='files/event_file.csv'
hostname_file=None #'files/ip_to_hostnames.txt'
interval='1S'
vlan_filter=None
protocol_filter=None
time_filter=None
analyze(event_traffic_csv, baseline_traffic_csv, event_file, hostname_file, interval, vlan_filter, protocol_filter, time_filter)