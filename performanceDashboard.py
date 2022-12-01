import webbrowser
import pandas as pd     
import plotly           #(version 4.5.0)
import plotly.express as px

import dash             #(version 1.8.0)
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State


# app = dash.Dash(__name__)
import plotly.figure_factory as ff



df = pd.read_csv("/Users/angelinelee/Downloads/mdl_h5pactivity_attempts-20221014-185632.csv")
df['duration per point'] = df['duration in seconds']/df['maxscore']

df['h5pactivityid'] = df['h5pactivityid'].astype(str)

df['h5pactivityid'].unique()

df.columns

app = dash.Dash(__name__)

app.layout = html.Div([ 

    html.Label(['Performance Dashboard'],style={'font-weight': 'bold', "text-align": "center", "font-size": "300%", "font-family": "verdana"}),


    html.Div([ 
        dcc.Graph(id = 'our_graph')
    ], className = 'nine columns'),


    html.Div([

        html.Br(),
        html.Label(['Choose Type of Graph'],style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='graph_type',
            options=["Histogram", "KDE Plots", "Duration Plots"],
            value='Histogram',
            multi=False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose Graph...',
            className='form-dropdown',
            style={'width':"90%"},
            persistence='string',
            persistence_type='memory'),
        html.Label(['Choose 3 Activities to Compare:'],style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='activity_one',
            options=[{'label':x, 'value':x} for x in df.sort_values('h5pactivityid')['h5pactivityid'].unique()],
            value='1',
            multi=False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose Activity...',
            className='form-dropdown',
            style={'width':"90%"},
            persistence='string',
            persistence_type='memory'),

        dcc.Dropdown(id='activity_two',
            options=[{'label':x, 'value':x} for x in df.sort_values('h5pactivityid')['h5pactivityid'].unique()],
            value='2',
            multi=False,
            clearable=False,
            persistence='string',
            persistence_type='session'),

        dcc.Dropdown(id='activity_three',
            options=[{'label':x, 'value':x} for x in df.sort_values('h5pactivityid')['h5pactivityid'].unique()],
            value='3',
            multi=False,
            clearable=False,
            persistence='string',
            persistence_type='local'),

    ],className='three columns'),


])

def histogram(first, second, third):
    df1 = df[(df["h5pactivityid"] == first) | (df["h5pactivityid"] == second)| (df["h5pactivityid"] == third)]
    fig = px.histogram(df1, x= "h5pactivityid")
    fig.update_layout(title_text = 'Distribution of h5activityid')
    return fig

def KDEplt(first, second, third):
    dff = df[(df['h5pactivityid'] == first) |
            (df['h5pactivityid'] == second) |
            (df['h5pactivityid'] == third)]


    group_labels = [first, second, third]

    data = dff[dff['h5pactivityid'] == first]
    data_1 = data['duration per point']
    data = dff[dff['h5pactivityid'] == second]
    data_2 = data['duration per point']
    data = dff[dff['h5pactivityid'] == third]
    data_3 = data['duration per point']


    hist_data = [data_1, data_2, data_3]       

    fig = ff.create_distplot(hist_data, group_labels, show_rug = False, show_hist = False)
    fig.update_layout(title_text = 'Distribution of durations obtained for different activities')
    return fig

def duration(first, second, third):
    dff = df[(df['h5pactivityid'] == first)]


    group_labels = [first]

    data = dff[dff['h5pactivityid'] == first]
    data_1 = data['rawscore (score received)']
    


    hist_data = [data_1]
      

    fig = ff.create_distplot(hist_data, group_labels, show_rug = False)
    fig.update_layout(title_text = 'Distribution of raw scores obtained for different activities')
    return fig

@app.callback(
    Output('our_graph','figure'),
    [Input('graph_type', 'value'),
     Input('activity_one','value'),
     Input('activity_two','value'),
     Input('activity_three','value')]
)

def build_graph(graph_type, first, second, third):

    fig = None
    
    if graph_type == "Histogram":

        fig = histogram(first, second, third)

    if graph_type == "KDE Plots":
        fig = KDEplt(first, second, third)
    
    if graph_type == "Duration Plots":
        fig = duration(first, second, third)

    return fig

if __name__ == '__main__':
    webbrowser.get('chrome').open('http://127.0.0.1:8050')
    app.run_server(debug=False)