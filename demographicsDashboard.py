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

df = pd.read_csv("/Users/angelinelee/Documents/get /mdl_h5pactivity_attempts-20221014-185632.csv")  
df['duration per point'] = df['duration in seconds']/df['maxscore']

df['h5pactivityid'] = df['h5pactivityid'].astype(str)

df = df[["duration per point", "h5pactivityid"]]
app = dash.Dash(__name__)


#_______________________________________________________________
#demographics visualizations
student = pd.read_csv("/Users/angelinelee/Downloads/mdl_student.csv", encoding = 'unicode_escape')
learner = pd.read_csv("/Users/angelinelee/Downloads/mdl_learner.csv", encoding = 'unicode_escape')
request_data = pd.read_csv("/Users/angelinelee/Downloads/learnerRequestData-1664008267.csv", encoding = 'unicode_escape')
# request_data.drop('School', 1)


#---------------------------------------------------------------

# df = pd.read_csv("/Users/angelinelee/Downloads/DOHMH_New_York_City_Restaurant_Inspection_Results.csv")  # https://drive.google.com/file/d/1jyvSiRjaNIeOCP59dUFQuZ0_N_StiQOr/view?usp=sharing
# df['INSPECTION DATE'] = pd.to_datetime(df['INSPECTION DATE'])
# df = df.groupby(['INSPECTION DATE','CUISINE DESCRIPTION','CAMIS'], as_index=False)['SCORE'].mean()
# df = df.set_index('INSPECTION DATE')
# df = df.loc['2016-01-01':'2019-12-31']
# df = df.groupby([pd.Grouper(freq="M"),'CUISINE DESCRIPTION'])['SCORE'].mean().reset_index()
# print (df[:5])

#---------------------------------------------------------------
app.layout = html.Div([

    html.Label(['Performance Dashboard'],style={'font-weight': 'bold', "text-align": "center", "font-size": "300%", "font-family": "verdana"}),

    html.Div([
        dcc.Graph(id='our_graph')
    ],className='nine columns'),

    html.Div([

        html.Br(),
        html.Label(['Choose Type of Graph'],style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='graph_type',
            options=["Student Gender Bar Charts", "Learner Gender Bar Charts", "Student Gender Distribution by Campus", "Learner Gender Distribution by Campus", "Learner Gender Distribution by Age", "Learner Age Histogram", "Student Class Histogram", "Student Section Histogram"],
            value='Student Gender Bar Charts',
            multi=False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose Graph...',
            className='form-dropdown',
            style={'width':"90%"},
            persistence='string',
            persistence_type='memory'),

    ],className='three columns'),

])

#---------------------------------------------------------------


def gender_bar(dataset):
    data = dataset["gender"].value_counts()
    fig = px.bar(data, color = px.colors.sequential.Blues[:data.size])
    return fig

def gender_hist(dataset):
    fig = px.histogram(dataset, x = "campus_id", color = "gender", barmode = 'group')
    return fig

def gender_age_hist(dataset):
    fig = px.histogram(dataset, x = "age", color = "gender", barmode = "group", nbins = 20, range_x = [0,100])
    return fig

def age_hist(dataset):
    fig = px.histogram(dataset, x = "age")
    return fig

def class_hist(dataset, type):
    fig = px.histogram(dataset, x = type)
    return fig

@app.callback(
    Output('our_graph','figure'),
    [Input('graph_type', 'value')]
)


def build_graph(graph_type):
    
    if graph_type == "Student Gender Bar Charts":
        fig = gender_bar(student)

    if graph_type == "Learner Gender Bar Charts":
        fig = gender_bar(learner)

    if graph_type == "Student Gender Distribution by Campus":
        fig = gender_hist(student)
    
    if graph_type == "Learner Gender Distribution by Campus":
        fig = gender_hist(learner)

    if graph_type == "Learner Gender Distribution by Age":
        fig = gender_age_hist(learner)
    
    if graph_type == "Learner Age Histogram":
        fig = age_hist(learner)
    
    if graph_type == "Student Class Histogram":
        fig = class_hist(request_data, "Class")
    
    if graph_type == "Student Section Histogram":
        fig = class_hist(request_data, "Section")

    return fig

#---------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=False)