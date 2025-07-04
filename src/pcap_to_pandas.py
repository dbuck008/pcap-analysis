# read pcap into pandas
import pandas as pd #sudo apt install python3-pandas

# ingest pcap into pandas
# analysis (magic)

print("Reading csv file into Pandas...")

def read_pcap_csv(pcap_csv_file_path):
    # read the csv
    df = pd.read_csv(pcap_csv_file_path, header=0, sep="\t")

    # clean the data
    df['frame.time_epoch'] = pd.to_datetime(df['frame.time_epoch'], unit='s')
    df['frame.len'] = df['frame.len'].astype(int)

    # df.set_index('frame.time_epoch', inplace=True)

    # # add vlans - todo: remove
    df['vlan.id'] = 1
    df.iloc[1::2].loc[:,'vlan.id']=2
    ####

    return df


