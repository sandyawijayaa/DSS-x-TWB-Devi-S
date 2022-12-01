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

#---------------------------------------------------------------
# change file paths here

df = pd.read_csv("/Users/angelinelee/Downloads/mdl_h5pactivity_attempts-20221014-185632.csv")
attempts = df.copy()
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
            options=["Duration Plots", "Score Plots", "Success Rate Table", "Mean Duration Table", "Mean Scores Table"],
            value="Duration Plots",
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

def duration(first, second, third):
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

def scores(first, second, third):
    dff = df[(df['h5pactivityid'] == first)]


    group_labels = [first]

    data = dff[dff['h5pactivityid'] == first]
    data_1 = data['rawscore (score received)']
    


    hist_data = [data_1]
      

    fig = ff.create_distplot(hist_data, group_labels, show_rug = False)
    fig.update_layout(title_text = 'Distribution of raw scores obtained for different activities')
    return fig

def success_rate():
    activityCount = attempts['h5pactivityid'].value_counts()
    attempts_table = activityCount.to_frame().sort_index(ascending=True)
    attempts_table

    # finding total successes
    filterSuccess = attempts['success if all question are answered correctly then its 1 otherwise 0'] == 1
    attempts.where(filterSuccess, inplace = True)
    success = attempts['h5pactivityid'].value_counts().astype(int)
    # success_table = success.to_frame().sort_index(ascending=True)

    # find success rate: success/attempts --> lower success rate = more difficult
    success_count = success / activityCount
    successrate_table = success_count.to_frame().sort_index(ascending=True)
    successrate_table.reset_index(inplace=True)
    successrate_table = successrate_table.rename(columns = {'index':'Activity ID', 'h5pactivityid':'Success Rate (%)'})

    successrate_table['Activity ID'] = successrate_table['Activity ID'].astype(int).astype(str)

    return px.bar(successrate_table, x = "Activity ID", y="Success Rate (%)", title = "Success Rate per Activity")

def mean_duration():
    grouped = attempts.groupby(['userid', 'h5pactivityid', 'duration in seconds'])['h5pactivityid'].size().reset_index(name='counts')
    # activitycount = grouped['h5pactivityid'].value_counts()
    mean_duration_by_activity = grouped.groupby(['h5pactivityid']).agg({'duration in seconds':'mean'})
    mean_duration_by_activity.reset_index(inplace=True)
    mean_duration_by_activity = mean_duration_by_activity.rename(columns = {'h5pactivityid':'Activity ID', 'duration in seconds':'Seconds'})
    # ax = px.bar(mean_duration_by_activity, x="Activity ID", y="Seconds")
    mean_duration_by_activity['Activity ID'] = mean_duration_by_activity['Activity ID'].astype(int).astype(str)

    return px.bar(mean_duration_by_activity, x = "Activity ID", y="Seconds", title = "Mean Duration in Seconds per Activity")

def mean_scores():
    grouped_scores = attempts.groupby(['userid', 'h5pactivityid', 'rawscore (score received)'])['h5pactivityid'].size().reset_index(name='counts')
    # mean_score_by_activity = grouped_scores.groupby(['h5pactivityid']).agg({'rawscore (score received)':'mean'})
    max_score_by_activity = grouped_scores.groupby(['h5pactivityid']).agg({'rawscore (score received)':'max'})

    max_score_by_activity = max_score_by_activity.reset_index()
    max_score_by_activity = max_score_by_activity.rename(columns = {'h5pactivityid':'Activity ID', 'rawscore (score received)':'Score'})
    max_score_by_activity.fillna(0)
    max_score_by_activity['Activity ID'] = max_score_by_activity['Activity ID'].astype(float).astype(int).astype(str)

    return px.bar(max_score_by_activity, x = "Activity ID", y="Score", title = 'Mean Score by Activity')



@app.callback(
    Output('our_graph','figure'),
    [Input('graph_type', 'value'),
     Input('activity_one','value'),
     Input('activity_two','value'),
     Input('activity_three','value')]
)

def build_graph(graph_type, first, second, third):
    fig = None

    if graph_type == "Duration Plots":
        fig = duration(first, second, third)
    
    if graph_type == "Score Plots":
        fig = scores(first, second, third)

    if graph_type == "Success Rate Table":
        fig = success_rate()

    if graph_type == "Mean Duration Table":
        fig = mean_duration()
    
    if graph_type == "Mean Scores Table":
        fig = mean_scores()

    return fig

if __name__ == '__main__':
    app.run_server(debug=False)