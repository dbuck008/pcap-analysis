# 🧰 PCAP Analysis Toolkit

This repository provides a suite of modular Python scripts to analyze network traffic extracted from PCAP files using pandas DataFrames. These tools support event-driven comparisons, baseline monitoring, and visualization of behavioral anomalies.

---

## 🔧 Features

- 📊 Bandwidth, packet count, and packet size tracking
- 🧠 Anomaly detection using entropy and z-score analysis
- 🧑‍💻 Top talkers, new conversations, lateral movement
- 🎯 Event annotation overlays and baseline comparisons
- 📡 Jitter and burst detection
- 🔐 Port and protocol anomaly tracking

---

## 📁 Project Structure

```
main.py
src/
├── bandwidth.py
├── burst_detection.py
├── lateral_movement_analysis.py
├── new_rare_conversations.py
├── packet_count.py
├── packet_size.py
├── pcap_to_pandas.py
├── plot_jitter_over_time.py
├── protocol_entropy.py
├── read_events.py
├── read_hostnames.py
├── top_talkers.py
├── unusual_ports_protocols.py
```

---

## 🔍 Function Documentation

### `analyze(...)`
> Orchestrates analysis using event and baseline data, VLAN and protocol filters, time windows, and hostname mapping.

---

### `read_pcap_csv(file)`
📍 `src/pcap_to_pandas.py`  
> Converts PCAP CSV export to pandas DataFrame.

**Why it matters:**  
Standardizes incoming data for consistent downstream processing. Ensures compatibility with all plotting and detection modules.

📍 `src/pcap_to_pandas.py`  
> Converts PCAP CSV export to pandas DataFrame. Foundation for all other analyses.

---

### `read_events(file)`
📍 `src/read_events.py`  
> Loads CSV annotations to mark known attack phases or operator events on graphs.

**Why it matters:**  
Overlays human or system-known events on metrics for context. Helps analysts correlate metric spikes with known testing or threat phases.

---

### `load_ip_hostname_mapping(file)`
📍 `src/read_hostnames.py`  
> Maps IP addresses to hostnames for clearer visuals and human-readability.

**Why it matters:**  
Improves interpretability of graphs and outputs by labeling infrastructure with recognizable names instead of raw IPs.

---

### `plot_bandwidth(...)`
📍 `src/bandwidth.py`  
> Plots total, per-VLAN, and per-protocol bandwidth.

**Why it matters:**  
Bandwidth changes can signal scanning, tunneling, data exfiltration, or DoS. Monitoring usage trends helps detect spikes, bottlenecks, and anomalies.

---

### `detect_bandwidth_bursts(...)`
📍 `src/burst_detection.py`  
> Detects short-duration traffic spikes using rolling z-scores. Flags potentially malicious transfer bursts.

**Why it matters:**  
Burst spikes may indicate malware behavior like beaconing or C2 communication. Statistical detection helps flag these subtle anomalies.

---

### `plot_packet_count(...)`
📍 `src/packet_count.py`  
> Packet frequency over time. Reveals scanning, flooding, or noisy applications.

**Why it matters:**  
High packet count may suggest scanning or flooding attacks. Detects noisy devices or protocols behaving abnormally.

---

### `plot_avg_packet_sizes(...)`
📍 `src/packet_size.py`  
> Tracks frame size trends. Indicates application shifts or tunneling.

**Why it matters:**  
Changes in packet size could indicate application switching or tunneling. Smaller sizes often correlate with beaconing, large with transfers.

---

### `compare_top_talkers(...)`, `compare_top_receivers(...)`
📍 `src/top_talkers.py`  
> Identifies top traffic generators/receivers. Flags pivot points or beaconing devices.

**Why it matters:**  
Highlights hosts of interest. Sudden changes in top talkers or receivers between baseline and event phases often signal compromised nodes or pivots.

---

### `plot_port_protocol_activity(...)`
📍 `src/unusual_ports_protocols.py`  
> Z-score anomaly detection for destination/source port or protocol usage shifts.

**Why it matters:**  
Unusual ports/protocols may indicate scanning or the use of non-standard services for covert channels.

---

### `calculate_protocol_entropy(...)`
📍 `src/protocol_entropy.py`  
> Computes Shannon entropy over time. Measures protocol diversity or consolidation during incidents.

**Why it matters:**  
Entropy reflects diversity of communication. Lower entropy may signal centralized C2 or restricted command channels.

---

### `plot_jitter(...)`
📍 `src/plot_jitter_over_time.py`  
> Measures jitter (variance in inter-packet time). Indicates instability or covert channels.

**Why it matters:**  
Detects timing inconsistencies that may point to obfuscated channels, proxy behavior, or time-based beaconing.

---

### `detect_new_or_rare_conversations(...)`
📍 `src/new_rare_conversations.py`  
> Flags conversations rare in baseline or new in event traffic. Detects malware pivoting or lateral movement.

**Why it matters:**  
New communications often indicate lateral movement, unauthorized access, or internal reconnaissance.

---

### `lateral_movement_analysis(...)`
📍 `src/lateral_movement_analysis.py`  
> Detects fan-out, port spray, and new connections across host/port axes.

**Why it matters:**  
Lateral movement is a key step in post-compromise activity. Identifying host-to-host expansion patterns helps spot attackers as they pivot.

---

## 🚀 Getting Started

1. Export PCAP data as CSV using `tshark` or another parser.
2. Customize or run `main.py` with your baseline and event CSVs.
3. Use annotations and IP label files to improve visibility.
4. View output plots or extend with new metrics.

---

## 🧩 Requirements

- Python 3.8+
- `pandas`, `numpy`, `matplotlib`

---

## To Run
The files in this 'pcap analysis' folder can be used to perform analysis on pcap files and display graphs with a variety of useful results. 

1. To run, you must first create a csv file from the pcap data in question
    a. I recommend merging all pcap files into one large pcap file, then using the built-in shell script, along with the files/param_list.txt file to generate the csv
    b. the files/param_list.txt file identifies all the meterics from the pcap file that you want to use for analysis. 
        i. It is strongly advised to not remove any metrics. Removing metrics may cause the analysis to fail. 
    c. to run the pcap_to_csv.sh script, do the following:
        i. Place the pcap file in the pcaps/ folder
        ii. Open a terminal
        iii. In terminal, navigate to the 'pcap analysis' folder
        iv.  run: ./pcap_to_csv.sh pcaps/input_file_name.pcap files/output_file_name.csv
2. Once you have a csv of the pcap you are interested in, you can modify the 'main.py' file in this folder to run the analysis you are interested in. Below is a highlevel view of the options
    a. bandwidth
    b. Packet rate
    c. average packet size
    d. top talkers
    e. unusal protocols and ports
    f. broadcast and multicast traffic
    g. scanning behavior
    h. new or rare connections
    i. jitter
    j. source ports
    k. destination ports
    l. latency
3. Optional files include:
    a. event_file.csv
    b. ip_to_hostnames.csv



####

steps:
1. create the files needed in files/
  a. ip_to_hostnames.txt
  b. param_list.txt
2. convert them to unix
  a. sudo dos2unix filename.txt
3. install the following:
  tshark
  python3 (I'm using 3.12)
  pandas
  matplotlib
  numpy
4. install extensions
  a. pylance
  b. python
  c. python debugger
5. Run the main() function
  a. make sure to update the parameters to your ones (not the deault ones)
