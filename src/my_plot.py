import pandas as pd #sudo apt install python3-pandas
import matplotlib.pyplot as plt
import matplotlib.axes as ax
from src.annotate_graph import *
import plotly.offline as py
import plotly.graph_objs as go
import plotly.express as px

# draws the event windows onto the graph
def add_events_to_graph(fig, y_max=1, events=None):    
    if events is None: return

    if type(fig) == ax.Axes:
        for _, event in events.iterrows():
            if pd.notnull(event['end_time']):
                fig.axvspan(event['start_time'], event['end_time'], color='red', alpha=0.2)
                fig.text(
                    event['start_time'],
                    fig.get_ylim()[1] * 0.999,
                    event['label'],
                    color='red',
                    fontsize=9,
                    verticalalignment='top'
                )
            else:
                fig.axvline(event['start_time'], color='red', linestyle='--', linewidth=1)
                fig.text(
                    event['start_time'],
                    fig.get_ylim()[1] * 0.999,
                    event['label'],
                    color='red',
                    rotation=90,
                    verticalalignment='top',
                    fontsize=9
                )
    if type(fig) == go.Figure:
        for _, event in events.iterrows():
            if pd.notnull(event['end_time']):
                fig.add_vline(x=event['start_time'])
                fig.add_annotation(
                    x=event['start_time'],
                    y=y_max,
                    text=event['label'],
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="red"
                )
            else:
                fig.add_vline(x=event['start_time'])
                fig.add_annotation(
                    x=event['start_time'],
                    y=y_max,
                    text=event['label'],
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="red"
                )



def plot_line(x, y, title, x_label, y_label, result='png', size=(12,4), save=True, save_path=None, events=None):
    filename = f'{save_path}{title.replace("\n", " - ")}'

    if result == 'png':
        # save the png using matplotlib 
        fig, ax = plt.subplots(figsize=size)
        ax.plot(x,y)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True)
        plt.tight_layout()

        add_events_to_graph(ax, events)

        if save:
            plt.savefig(f'{filename}.png')
            plt.close()
        else:
            plt.show()

    elif result == 'html':
        # save fig as html to view in webbrowser later
        f = go.Figure()
        f.add_trace(go.Line(x=x, y=y))
        f.update_layout(title={'text': title, 'x': 0.5, 'xanchor': 'center'}, 
                        xaxis_title=x_label, 
                        yaxis_title=y_label)
        add_events_to_graph(f, y_max= y.max(), events=events)
        py.plot(f, filename=f'{filename}.html', auto_open=False)

def plot_pivot(pivot, title, x_label, y_label, result='png', size=(12,4), save=True, save_path=None, events=None):
    filename = f'{save_path}{title.replace("\n", " - ")}'

    if result == 'png':
        # save the png using matplotlib 
        ax = pivot.plot(figsize=size)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True)
        plt.tight_layout()

        add_events_to_graph(ax, events)

        if save:
            plt.savefig(f'{filename}.png')
            plt.close()
        else:
            plt.show()

    elif result == 'html':
        # save fig as html to interact with
        f = px.line(pivot, x=pivot.index, y=pivot.columns)
        add_events_to_graph(f, y_max=pivot.max().max(), events=events)
        f.update_layout(title={'text': title, 'x': 0.5, 'xanchor': 'center'}, 
                        xaxis_title=x_label, 
                        yaxis_title=y_label)
        py.plot(f, filename=f'{filename}', auto_open=False)