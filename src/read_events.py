import pandas as pd

# load event file
def read_events(event_file):
    events = pd.read_csv(event_file, parse_dates=['start_time', 'end_time'], keep_default_na=False, date_format='%Y-%m-%d %H:%M:%S')
    events['start_time'] = pd.to_datetime(events['start_time'], unit='s', errors='coerce')
    events['end_time'] = pd.to_datetime(events['end_time'], unit='s', errors='coerce')
    return events