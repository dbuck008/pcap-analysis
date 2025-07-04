import pandas as pd

# draws the event windows onto the graph
def add_events_to_graph(ax, events):    
    if events is not None:
        for _, event in events.iterrows():
            if pd.notnull(event['end_time']):
                ax.axvspan(event['start_time'], event['end_time'], color='red', alpha=0.2)
                ax.text(
                    event['start_time'],
                    ax.get_ylim()[1] * 0.999,
                    event['label'],
                    color='red',
                    fontsize=9,
                    verticalalignment='top'
                )
            else:
                ax.axvline(event['start_time'], color='red', linestyle='--', linewidth=1)
                ax.text(
                    event['start_time'],
                    ax.get_ylim()[1] * 0.999,
                    event['label'],
                    color='red',
                    rotation=90,
                    verticalalignment='top',
                    fontsize=9
                )