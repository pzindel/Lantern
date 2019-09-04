#import libraries
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np

#import supporting python scripts
from app import app
from apps.aggregated_app import *
from apps.data_app import *
from apps.exercise_app import *
from apps.floors_app import *
from apps.heart_app import *
from apps.sleep_app import *
from apps.step_app import *
from apps.summary_app import *

#server
server_system = False

app.layout = html.Div([
	dcc.Location(id='url', refresh=False),
	html.Div(id='page-content')
])

index_page = html.Div([
	html.Header(html.H1('Samsung Health App Data')),
	html.H3('Contents:'),
	html.Div([
		html.H6(dcc.Link('Summary', href='/summary')),
		html.Br(),
		html.H6(['1. ', dcc.Link('Sleep Analysis', href='/sleep')]),
		html.H6(['2. ', dcc.Link('Step Count Analysis', href='/step')]),
		html.H6(['3. ', dcc.Link('Floors Climbed Analysis', href='/floors')]),
		html.H6(['4. ', dcc.Link('Heart Rate Analysis', href='/heart')]),
		html.H6(['5. ', dcc.Link('Exercise Analysis', href='/exercise')]),
		html.H6(['6. ', dcc.Link('Daily Aggregated Analysis', href='/daily_aggregated')]),
		html.H6(['A. ', dcc.Link('Data Sets', href='/data')])
	], style={'padding-left':'5%'}),
])


#Update the displayed page
@app.callback(
	Output('page-content', 'children'),
	[Input('url', 'pathname')]
)
def display_page(pathname):
	if pathname == '/summary':
		return summary_page
	elif pathname == '/sleep':
		return sleep_page
	elif pathname == '/step':
		return step_page
	elif pathname == '/floors':
		return floors_page
	elif pathname == '/heart':
		return heart_page
	elif pathname == '/exercise':
		return exercise_page
	elif pathname == '/daily_aggregated':
		return aggregated_page
	elif pathname == '/data':
		return data_page
	else:
		return index_page

if __name__ == '__main__':
	if server_system:
		app.run_server(debug=True, port=5000, host='10.162.0.2')
	else:
		app.run_server(debug=True)