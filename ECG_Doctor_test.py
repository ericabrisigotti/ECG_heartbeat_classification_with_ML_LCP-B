# we import the packages needed for plotting with Plotly Dash
import pandas as pd
import numpy as np

from dash import Dash, html, dcc, callback, Output, Input, Patch
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# we choose which file we want to import
path='01'
# and import it a dataframe 
df_ = pd.read_csv('output_files/'+'data'+path+'_filtered.csv')
# and also import the dataframe with information about all the heartbeats (of all patients)
hb_ = pd.read_csv('output_files/'+'heartbeats.csv')
# and take only its rows relevant to the chosen patient
hb_ = hb_[hb_['patient']==int(path)]

# we choose the number of ill heartbeats to display
n_hb_ill=25
# we identify the ill heartbeats
hb_mask = hb_['ann_symbol']!='N'
hb_ill = hb_[hb_mask]
# ???? (we should be randomly sampling this as well)
hb_ill = hb_ill.iloc[:n_hb_ill]

# we choose the number of healthy heartbeats to display
n_hb_normal=25
# ???? (why do we reference ill for healthy)
hb_N = hb_[:hb_ill.index[-1]]
# we identify the healthy heartbeats
hb_mask_N = hb_N['ann_symbol']=='N'
hb_N = hb_N[hb_mask_N]
# and randomly sample based on the chosen number
hb_N = hb_N.sample(n_hb_normal)

# we save the heartbeats together
hb = pd.concat([hb_ill, hb_N])
# and scrumble them
hb = hb.sort_index()

# ????
df = df_.iloc[0:hb['ann_index'].values[-1]+1]

# we set the quantities needed for plotting
# - the indexes i.e. values for the x-axis
x = np.arange(0, len(df), 1)
# - the dataframe with the signal in all leads
df = df
# - the name of all leads
names = list(df.columns.values)
# - the colors to use to represent the signal in all leads
colors = ['salmon', 'darkorange', 
          'gold', 'khaki', 
          'lawngreen', 'limegreen', 
          'springgreen', 'aquamarine', 
          'mediumturquoise', 'lightskyblue',
          'mediumpurple', 'violet']
# - the xlimits for each heartbeat
starts = list(hb['start'].values)
ends =  list(hb['end'].values)
# ????
heartbeats = {"all": "All"}
heartbeats.update({i: f"beat {i}" for i in range(len(starts))})

# - the ML predictions
df["ml"] = ""
ann_pos = list(hb['ann_index'].values)
df.loc[ann_pos, "ml"] = hb['ann_symbol'].values

fig_ecg = make_subplots(
    rows=6, cols=2,
    shared_xaxes=True,
    #row_titles=names,
    x_title="Time"
)
        
for i, n in enumerate(names):
    if ((i+1)%2)==1:
        
        y = df[n]
        fig_ecg.append_trace(go.Scatter(x=x, y=df[n], marker_color=colors[i], name=n),row=int((i + 2)/2), col=1)
        fig_ecg['layout']['yaxis{}'.format(i+1)]['title']=n
    else: 
        y = df[n]
        fig_ecg.append_trace(go.Scatter(x=x, y=df[n], marker_color=colors[i], name=n), row=int((i + 1)/2), col=2)
        fig_ecg['layout']['yaxis{}'.format(i+1)]['title']=n
#fig_ecg['layout']['yaxis{}'.format(i)]['title']=n
    
    
fig_ecg.update_layout(title_text="", height=1000)
#fig_ecg.update_yaxes(showticklabels=False)

fig_ecg.update_yaxes(title_text=names, secondary_y=True, showticklabels=False)   

# %%
app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1("ECG"),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(heartbeats, id="dropdown", value="all")
                    ],
                    style={'padding': 10, 'flex': 1}
                ),
                html.Div(
                    [
                        dcc.Checklist(
                            {"ML": "Show ML annotations"}, id="checkbox", value=[])
                    ],
                    style={'padding': 10, 'flex': 1}
                )
            ],
            style={'display': 'flex', 'flex-direction': 'row'}
        ),
        dcc.Graph(figure=fig_ecg, id="ecg"),
    ]
)

# %% callbacks
# update the plots with the specific heartbeat x range

@callback(
    Output("ecg", "figure"),
    Input("dropdown", "value"),
    Input("checkbox", "value") )

def update(dropdown, checkbox):
    # extract data from df within the heartbeat range
    if dropdown == "all":
        ddf = df
        range = x
    else:
        dropdown = int(dropdown)
        mask = (x > starts[dropdown]) & (x < ends[dropdown])
        ddf = df.loc[mask]
        range = x[mask]

    # ML annotation
    mode = "lines+text" if checkbox else "lines"

    # redo the plot
    figure = make_subplots(
    rows=6, cols=2,
    shared_xaxes=True,
    #row_titles=names,
    x_title="Time")
        
    for i, n in enumerate(names):
        if ((i+1)%2)==1:

            y = df[n]
            figure.append_trace(go.Scatter(x=range, y=ddf[n], marker_color=colors[i], name=n, mode=mode, 
                                text=ddf["ml"]),
                                row=int((i + 2)/2), col=1)
            figure['layout']['yaxis{}'.format(i+1)]['title']=n
        else: 
            y = df[n]
            figure.append_trace(go.Scatter(x=range, y=ddf[n], marker_color=colors[i], name=n, mode=mode, text=ddf["ml"]), 
                                row=int((i + 1)/2), col=2)
            figure['layout']['yaxis{}'.format(i+1)]['title']=n



    figure.update_layout(title_text="", height=1000)
    figure.update_yaxes(title_text=names, secondary_y=True, showticklabels=False)     
    #figure.update_traces(textposition='top right')

    return figure

# try: 
if  __name__ == '__main__':
        app.run(debug=False,port=8000)
# except:
#     print("Exception occured!")
#     from werkzeug.serving import run_simple
#     run_simple('localhost', 10, app)