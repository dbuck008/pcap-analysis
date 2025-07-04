import pandas as pd

def detect_new_or_rare_conversations(df_baseline, df_event, rare_threshold=3):
    # need to look at the data and change the threshold base on what we see
    
    def get_conversations(df):
        conv = df.groupby(['ip.src', 'ip.dst', 'ip.proto']).size().reset_index(name='count')
        return conv

    base_convs = get_conversations(df_baseline)
    event_convs = get_conversations(df_event)

    # Merge on flow key
    merged = pd.merge(
        base_convs,
        event_convs,
        on=['ip.src', 'ip.dst', 'ip.proto'],
        how='outer',
        suffixes=('_baseline', '_event')
    ).fillna(0)

    merged['is_new'] = (merged['count_baseline'] == 0) & (merged['count_event'] > 0)
    merged['is_rare'] = (merged['count_baseline'] > 0) & (merged['count_baseline'] <= rare_threshold) & (merged['count_event'] > merged['count_baseline'])

    return merged[merged['is_new'] | merged['is_rare']].sort_values('count_event', ascending=False)
