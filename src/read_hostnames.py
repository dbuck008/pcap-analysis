import pandas as pd

def load_ip_hostname_mapping(filepath):
    df_map = pd.read_csv(filepath, header=0)
    return dict(zip(df_map['ip'], df_map['hostname']))