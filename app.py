import os
import json
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
from flask import Flask
from pandas_datareader import data as web
from datetime import datetime as db
import xlrd

server = Flask(__name__)


import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt


travel = pd.read_csv('data/Date_brazil.csv', index_col='Date', encoding = "ISO-8859-1")

app = dash.Dash('Brazil')


app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.layout = html.Div([html.Div([html.H2('Tourist visitors to Brazil'),
                       html.P("Total number of people visited to the country = 108889535.0"),]),

html.Div([
    html.Div([html.H4('Worldwide Inflow of Visitors to Brazil'),
              html.P("Use slider to See the flow"),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=travel['Year'].min(),
        max=travel['Year'].max(),
        value=travel['Year'].min(),
        step=None,
        marks={str(year): str(year) for year in travel['Year'].unique()})
    ],style={'width': '55%', 'float': 'right'}, className="container"),

html.Div([html.H4('Monthly Distribution of Visitors'),
          html.P("Select the Dropdown Menu to See Monthly Distribution"),
          dcc.Dropdown(
              id='my-dropdown',
              options=[
                  {'label': 'January', 'value': 1},
                  {'label': 'February', 'value': 2},
                  {'label': 'March', 'value': 3},
                  {'label': 'April', 'value': 4},
                  {'label': 'May', 'value': 5},
                  {'label': 'June', 'value': 6},
                  {'label': 'July', 'value': 7},
                  {'label': 'August', 'value':8},
                  {'label': 'Septmenber', 'value': 9},
                  {'label': 'October', 'value': 10},
                  {'label': 'November', 'value': 11},
                  {'label': 'December', 'value': 12}
              ],
              value='January'
          ),
          dcc.Graph(id='month-graph')
         ],
         style={'width': '40%'}),

html.Div([
    html.Div([
        html.H5('Visitor Distribution by Mode of Transport'),
        html.P("Select option of transport"),
        dcc.RadioItems(id='transport_id',options=[{'label': i, 'value': i} for i in ['Air', 'Land', 'River', 'Sea']],
                       value='Air',
                       labelStyle={'display': 'inline-block'}
                      ),
        dcc.Graph(figure={'data': [{'x':[1,2], 'y': [3, 1]}]}, id='way-graph'),
    ],
        style={'width': '55%','float': 'right', 'display': 'inline-block'}),
    html.Div([
        html.H5('Distribution of Visitors by Country'),
        html.P("Enter a country name"),
        dcc.Input(placeholder='Enter a country name', value='Argentina', id='my-Input', type = 'text'),
        dcc.Graph(figure={'data': [{'x':[1,2], 'y': [3, 1]}]}, id='Country-graph'),
    ],
        style={'width': '40%'}),
]),

html.Div([

    html.Div([html.H4('Chorolepath Map View of Visitors by Origin to Brazil'),
              html.Iframe(src="https://dattatele.github.io/url_data/tourist.html", width="100%", height="500" )],
             ),

    html.Div([html.H4('Overall % Distribution of Transport'),
              html.Iframe(src="https://dattatele.github.io/url_data/pie_Chart_transport.html", width="50%", height="500")],
            style={'float': 'center'})


])
])
])


@app.callback(dash.dependencies.Output('graph-with-slider', 'figure'),
              [dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = travel[travel.Year == selected_year]
    traces = []
    for i in filtered_df.Continent.unique():
        travel_by_continent = filtered_df[filtered_df['Continent'] == i]
        traces.append(go.Scatter(
            y=travel_by_continent['Count'],
            text=travel_by_continent['Country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            yaxis={'title': 'Number of visitors flow', 'range': [5, 100]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

@app.callback(Output('month-graph', 'figure'), [Input('my-dropdown', 'value')])

def update_graph(selected_dropdown_value):
    dff = travel.loc[travel['Month'] == selected_dropdown_value, "Count"]
    month_df = dff.groupby(dff.index, sort=False).sum()
    return {
        'data': [{
            'x': month_df.index,
            'y': month_df
        }],
            'layout': {'margin': {'l': 50, 'r': 5, 't': 20, 'b': 65}}
    }
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})


@app.callback(Output('Country-graph', 'figure'), [Input('my-Input', 'value')])
def update_graph(input_value):
    fake = travel.loc[travel['Country'] == input_value, "Count"]
    country_df = fake.groupby(fake.index, sort=False).sum()
    return {
        'data': [{
            'x': country_df.index,
            'y': country_df
        }],
        'layout': {'margin': {'l': 50, 'r': 5, 't': 20, 'b': 70}}
    }

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})


@app.callback(
    dash.dependencies.Output('way-graph', 'figure'),
    [dash.dependencies.Input('my-Input', 'value'),
     dash.dependencies.Input('transport_id', 'value')])
def update_graph(selected_input, transport_id_name):
    second_way = travel.loc[(travel['Country'] == selected_input) & (travel["WayIn"] == transport_id_name)]
    way_out = second_way.loc[second_way['WayIn'] == transport_id_name, "Count"]
    correct_way = way_out.groupby(way_out.index, sort=False).sum()
    return {
        'data': [{
            'x': correct_way.index,
            'y': correct_way
        }],
        'layout': {'margin': {'l': 50, 'r': 5, 't': 20, 'b': 70}}
    }

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

app.component_suites = [
    'dash_core_components',
    'dash_html_components'
]


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.server.run('0.0.0.0', port=port)
