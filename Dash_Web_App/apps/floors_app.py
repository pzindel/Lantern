#import libraries
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np

#import supporting python scripts
from app import app

#import data files
floors_df = pd.read_csv("cleaned_data/floors_climbed_cleaned.csv", sep=',', index_col=0)

#cast to datetime object
floors_df['local_start_time'] = pd.to_datetime(floors_df['local_start_time'])
floors_df['local_end_time'] = pd.to_datetime(floors_df['local_end_time'])

floors_plot_types = {
	'Histogram': ['Floors Climbed'],
	'Scatter': ['Floors vs Time'],
	'Boxplot': ['Floors vs Weekday'],
}

floors_page = html.Div([
	html.Header([
		' | ',
		dcc.Link('Home', href='/'), ' | ',
		dcc.Link('Summary', href='/summary'), ' | ',
		dcc.Link('Sleep', href='/sleep'), ' | ',
		dcc.Link('Step Count', href='/step') , ' | ',
		dcc.Link('Floors Climbed', href='/floors'), ' | ',
		dcc.Link('Heart Rate', href='/heart'), ' | ',
		dcc.Link('Exercise', href='/exercise'), ' | ',
		dcc.Link('Daily Aggregated', href='/daily_aggregated'), ' | ',
		dcc.Link('Data Sets', href='/data'), ' | '
	], id='top', style={'textAlign':'center'}),
	html.Br(),
	html.Div([
		html.H1('Floors Climbed Analysis'),
		html.Div([
			html.H3("Preparing the data sets:"),
			html.P(["One of the data sets produced by the Samsung Health App is a record of the floors climbed by the user when climbing stairts. The values retained for this analysis are: ", html.Br(),
				"	- the start time and end time (in UTC date-time format),", html.Br(),
				"	- the user's UTC time zone offset at the time of recording,", html.Br(),
				"	- the number of floors climbed (taking 3m per floor),", html.Br(),
				"	- the device ID (tracking which device recorded the data).", html.Br(), html.Br(),
				"The additional values recorded in the data which were removed for the analysis, because they either contained no new or useful information, \
					(and reason for removal) are:", html.Br(),
				"	- creation time & update time (provide no revelant information that is not already provided by the start & end time values),", html.Br(),
				"	- unique enrty ID (integer index used instead),", html.Br(), 
				"	- app internal package name (same for all entries; main use for developer purposes),", html.Br(), 
				"	- custom (value is empty for all entries),", html.Br(), html.Br(),
				"After removal of the mentioned values, the given start and end times (initially recorded in date-time UTC) were converted to a date-time format \
					localized to the user based on the recorded UTC time zone offset (which also takes into account daylight savings time observed during a \
					certain period of the year).", html.Br(), html.Br(), html.Br(),
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			html.H3("Results"),
			html.Br(), 
			html.Div([
				dcc.Dropdown(
					id='floors_plot_type',
					options=[{'label':i, 'value':i} for i in floors_plot_types.keys()],
					placeholder='Select plot type',
					value='Histogram',
				),
				dcc.Dropdown(
					id='floors_plot_data',
					placeholder='Select data to plot',
					value='Floors Climbed',
				),
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			dcc.Graph(
				id='floors_graphic',
			),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			html.Br(),
			html.P(["The number of floors climbed by the user are primarly 1 and 2 stories with the occassionaly higher story climbs. Futhermore, the number of floors \
					climbed is fairly consistent throughout the year, but with fewer mid- and high-story climbs in the summer months with the except of some entries \
					in September. The time zone data for those exceptions shows that the user was tavelling and perhaphs went sightseeing or happen upon a broken \
					elevator and had to make a high-story climb.", html.Br(),
				"Checking the spread of floors climbed throughout a given week we see that the users Saturday consists of a greater average of floors climbed and \
					a larger spread which may be a result of the user making fewer climbs on a Saturday resulting in a larger spread of few entries as compared to the \
					other days of the week.", html.Br(),
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
	], id='floors_analysis'),
	html.Br(),
	html.H6(['Go to ', html.A('top', href='#top')], style={'textAlign':'center'}),
	html.Footer([
		' | ',
		dcc.Link('Home', href='/'), ' | ',
		dcc.Link('Summary', href='/summary'), ' | ',
		dcc.Link('Sleep', href='/sleep'), ' | ',
		dcc.Link('Step Count', href='/step') , ' | ',
		dcc.Link('Floors Climbed', href='/floors'), ' | ',
		dcc.Link('Heart Rate', href='/heart'), ' | ',
		dcc.Link('Exercise', href='/exercise'), ' | ',
		dcc.Link('Daily Aggregated', href='/daily_aggregated'), ' | ',
		dcc.Link('Data Sets', href='/data'), ' | '
	], style={'textAlign':'center'})
]) 


#update the dropdown options depending on the selected graph type
@app.callback(
	Output('floors_plot_data', 'options'),
	[Input('floors_plot_type', 'value')])
def set_floors_plot_data(selected_plot):
	return [{'label':i, 'value':i} for i in floors_plot_types[selected_plot]]
	
#update the displayed graph depending on dropdown value
@app.callback(
    Output('floors_graphic', 'figure'),
    [Input('floors_plot_data', 'value')])
def update_floors_plot(plot):
	#histograms
	if plot == 'Floors Climbed':
		return {
			'data': [go.Histogram(
					x = floors_df[floors_df['time_offset'] == 'UTC-0800']['floor'],
					name = 'UTC-0800',
				),
				go.Histogram(
					x = floors_df[floors_df['time_offset'] == 'UTC-0500']['floor'],
					name = 'UTC-0500',
				),
				go.Histogram(
					x = floors_df[floors_df['time_offset'] == 'UTC-0400']['floor'],
					name = 'UTC-0400',
				),
				go.Histogram(
					x = floors_df[floors_df['time_offset'] == 'UTC+0200']['floor'],
					name = 'UTC+0200',
				),
			],
			'layout': go.Layout(
				title = 'Floors Climbed Distribution',
				xaxis = {'title': 'Floors Climbed'},
				yaxis = {'title': 'Frequency'},
				barmode='stack',
				hovermode = 'closest'
			)
		}
	
	#scatter plots
	if plot == 'Floors vs Time':
		return {
			'data': [go.Scatter(
					x = floors_df[floors_df['time_offset'] == 'UTC-0800']['local_start_time'],
					y = floors_df[floors_df['time_offset'] == 'UTC-0800']['floor'],
					name = 'UTC-0800',
					mode = 'markers',
				),
				go.Scatter(
					x = floors_df[floors_df['time_offset'] == 'UTC-0500']['local_start_time'],
					y = floors_df[floors_df['time_offset'] == 'UTC-0500']['floor'],
					name = 'UTC-0500',
					mode = 'markers',
				),
				go.Scatter(
					x = floors_df[floors_df['time_offset'] == 'UTC-0400']['local_start_time'],
					y = floors_df[floors_df['time_offset'] == 'UTC-0400']['floor'],
					name = 'UTC-0400',
					mode = 'markers',
				),
				go.Scatter(
					x = floors_df[floors_df['time_offset'] == 'UTC+0200']['local_start_time'],
					y = floors_df[floors_df['time_offset'] == 'UTC+0200']['floor'],
					name = 'UTC+0200',
					mode = 'markers',
				),
			],
			'layout': go.Layout(
				title = 'Floors Climbed over Time',
				xaxis = {'title': 'Time (year)'},
				yaxis = {'title': 'Floors Climbed'},
				hovermode = 'closest'
			)
		}


	
	#boxplots
	if plot == 'Floors vs Weekday':
		return {
			'data': [go.Box(
					y = floors_df[floors_df['local_start_time'].dt.dayofweek == 0]['floor'],
					name = 'Monday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = floors_df[floors_df['local_start_time'].dt.dayofweek == 1]['floor'],
					name = 'Tuesday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = floors_df[floors_df['local_start_time'].dt.dayofweek == 2]['floor'],
					name = 'Wednesday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = floors_df[floors_df['local_start_time'].dt.dayofweek == 3]['floor'],
					name = 'Thursday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = floors_df[floors_df['local_start_time'].dt.dayofweek == 4]['floor'],
					name = 'Friday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = floors_df[floors_df['local_start_time'].dt.dayofweek == 5]['floor'],
					name = 'Saturday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = floors_df[floors_df['local_start_time'].dt.dayofweek == 6]['floor'],
					name = 'Sunday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
			],
			'layout': go.Layout(
				title = 'Floors Climbed per Weekday',
				xaxis = {'title': 'Weekday'},
				yaxis = {'title': 'Floors Climbed'},
				hovermode = 'closest'
			)
		}

