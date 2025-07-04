from src.annotate_graph import *
import matplotlib.pyplot as plt

def plot_bandwidth_trace(x_data, y_data, title, x_label='Time', y_label='Mbps', save=False, save_path=None, events=None):
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(x_data, y_data)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.tight_layout()

    if events: add_events_to_graph(ax, events)

    if save:
        filename = f'{save_path}_{title}.png'
        plt.savefig(filename)
    else:
        plt.show()
    
    return fig