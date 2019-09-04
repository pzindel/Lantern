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
heart_rate_df = pd.read_csv("cleaned_data/heart_rate_cleaned.csv", sep=',', index_col=0)

#cast to datetime object
heart_rate_df['local_start_time'] = pd.to_datetime(heart_rate_df['local_start_time'])
heart_rate_df['local_end_time'] = pd.to_datetime(heart_rate_df['local_end_time'])

#add time zone float to heart_df
def to_float(x):
    return float(x[1])/100
heart_rate_df['hr_offset'] = heart_rate_df['time_offset'].str.split('UTC').apply(to_float)

heart_plot_types = {
	'Histogram': ['Heart Rate'],
	'Line': ['Time Offset vs Time'],
	'Boxplot': ['Hear Rate vs Weekday', 'Heart Rate vs Time of Day'],
}

heart_page = html.Div([
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
		html.H1('Heart Rate Analysis'),
		html.Div([
			html.H3("Preparing the data sets:"),
			html.P(["One of the data sets produced by the Samsung Health App is a record of the user's heart rate. The values retained for this analysis are: ", html.Br(),
				"	- the start time and end time of recording (in UTC date-time format),", html.Br(),
				"	- the user's UTC time zone offset at the time of recording,", html.Br(),
				"	- the user's bpm heart rate during recording,", html.Br(),
				"	- the maximum heart rate during recording,", html.Br(),
				"	- the minimum heart rate during recording,", html.Br(),
				"	- the device ID (tracking which device recorded the data).", html.Br(), html.Br(),
				"The additional values recorded in the data which were removed for the analysis, because they either contained no new or useful information, \
					(and reason for removal) are:", html.Br(),
				"	- binning data (continuous heart rate record; pointer to external json files which weren't present),", html.Br(),
				"	- total heart beat count for recoding (is binary and corresponds with device used for recording; i.e. removed for redundancy),", html.Br(),
				"	- creation time & update time (provide no revelant information that is not already provided by the start & end time values),", html.Br(),
				"	- unique enrty ID (integer index used instead),", html.Br(), 
				"	- app internal package name (same for all entries; main use for developer purposes),", html.Br(), 
				"	- comment & custom (both values are empty for each entry),", html.Br(),
				"After removal of the mentioned values, the given start and end times (initially recorded in date-time UTC) were converted to a date-time format \
					localized to the user based on the recorded UTC time zone offset (which also takes into account daylight savings time observed during a \
					certain period of the year). It was also found that two entries in the set were marked with an incorrect timestamp and were thus removed.", html.Br(), html.Br(), html.Br(),
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			html.H3("Results"),
			html.Br(),
			html.Div([
				dcc.Dropdown(
					id='heart_plot_type',
					options=[{'label':i, 'value':i} for i in heart_plot_types.keys()],
					placeholder='Select plot type',
					value='Histogram',
				),
				dcc.Dropdown(
					id='heart_plot_data',
					placeholder='Select data to plot',
					value='Heart Rate',
				),
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			dcc.Graph(
				id='heart_graphic',
			),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			html.Br(),
			html.P(["For this data set is to see whether the user has any abnormal heart rate entries which could be an indicator of the user's age or health. Starting \
					with a distribution of the heart rate measured we see log-normal type distribution centered around 60 beats per minute and trailing off up to 170 bpm. \
					The graph shows that the user's heart rate in a range we expect from a health and active person, and the higher bpm entries can presumably by from the \
					having exercised to elevate their hearth rate.", html.Br(),
				"Looking at the spread of the data across weekday shows a consistent heart rate every day, as expected based on the distribution. We also see that Wednesday, \
					Saturday, and Sunday have fewer high heart rate entries suggesting that when the user exercises on these days they're less likely to give their full effort.\
					Additionally, we can look at the spread of data across the time of day to see that the user is more likely to engage in exercise in the evening than in the \
					mornings.", html.Br(),
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
	], id='heart_analysis'),
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
	Output('heart_plot_data', 'options'),
	[Input('heart_plot_type', 'value')])
def set_heart_plot_data(selected_plot):
	return [{'label':i, 'value':i} for i in heart_plot_types[selected_plot]]

#update the displayed graph depending on dropdown value
@app.callback(
    Output('heart_graphic', 'figure'),
    [Input('heart_plot_data', 'value')])
def update_heart_plot(plot):
	#histograms
	if plot == 'Heart Rate':
		return {
			'data': [go.Histogram(
					x = heart_rate_df[heart_rate_df['time_offset'] == 'UTC-0800']['heart_rate'],
					name = 'UTC-0800',
				),
				go.Histogram(
					x = heart_rate_df[heart_rate_df['time_offset'] == 'UTC-0700']['heart_rate'],
					name = 'UTC-0700',
				),
				go.Histogram(
					x = heart_rate_df[heart_rate_df['time_offset'] == 'UTC-0500']['heart_rate'],
					name = 'UTC-0500',
				),
				go.Histogram(
					x = heart_rate_df[heart_rate_df['time_offset'] == 'UTC-0400']['heart_rate'],
					name = 'UTC-0400',
				),
				go.Histogram(
					x = heart_rate_df[heart_rate_df['time_offset'] == 'UTC+0200']['heart_rate'],
					name = 'UTC+0200',
				),
				go.Histogram(
					x = heart_rate_df[heart_rate_df['time_offset'] == 'UTC+0430']['heart_rate'],
					name = 'UTC+0430',
				),
			],
			'layout': go.Layout(
				title = 'Heart Rate Distribution',
				xaxis = {'title': 'Heart Rate (bpm)'},
				yaxis = {'title': 'Frequency'},
				barmode='stack',
				hovermode = 'closest'
			)
		}
	
	#line plot
	if plot == 'Time Offset vs Time':
		chron_sort_df = heart_rate_df.sort_values(by='local_start_time', axis=0, ascending=True)
		return {
			'data': [go.Scatter(
				x = chron_sort_df['local_start_time'],
				y = chron_sort_df['hr_offset'],
				name = plot,
				mode = 'lines+markers',
			)],
			'layout': go.Layout(
				title = 'Time Zone over Time',
				xaxis = {'title': 'Time (year)'},
				yaxis = {'title': 'Time Zone (UTC)'},
				hovermode = 'closest'
			)
		}
	
	#boxplots
	if plot == 'Hear Rate vs Weekday':
		return {
			'data': [go.Box(
					y = heart_rate_df[heart_rate_df['local_start_time'].dt.dayofweek == 0]['heart_rate'],
					name = 'Monday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = heart_rate_df[heart_rate_df['local_start_time'].dt.dayofweek == 1]['heart_rate'],
					name = 'Tuesday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = heart_rate_df[heart_rate_df['local_start_time'].dt.dayofweek == 2]['heart_rate'],
					name = 'Wednesday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = heart_rate_df[heart_rate_df['local_start_time'].dt.dayofweek == 3]['heart_rate'],
					name = 'Thursday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = heart_rate_df[heart_rate_df['local_start_time'].dt.dayofweek == 4]['heart_rate'],
					name = 'Friday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = heart_rate_df[heart_rate_df['local_start_time'].dt.dayofweek == 5]['heart_rate'],
					name = 'Saturday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = heart_rate_df[heart_rate_df['local_start_time'].dt.dayofweek == 6]['heart_rate'],
					name = 'Sunday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
			],
			'layout': go.Layout(
				title = 'Heart Rate per Weekday',
				xaxis = {'title': 'Weekday'},
				yaxis = {'title': 'Heart Rate (bpm)'},
				hovermode = 'closest'
			)
		}
	elif plot == 'Heart Rate vs Time of Day':
		return {
			'data': [{
					'y': heart_rate_df[heart_rate_df['local_start_time'].dt.hour == i]['heart_rate'],
					'name': str(i),
					'type': 'box',
					'boxpoints': 'outliers',
					'boxmean': 'sd',
				} for i in range(23)
			],
			'layout': go.Layout(
				title = 'Heart Rate per Time of Day',
				xaxis = {'title': 'Time of Day (hr)'},
				yaxis = {'title': 'Heart Rate (bpm)'},
				hovermode = 'closest'
			)
		}
