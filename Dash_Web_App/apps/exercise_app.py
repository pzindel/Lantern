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
exercise_df = pd.read_csv("cleaned_data/exercise_cleaned.csv", sep=',', index_col=0)

#cast to datetime object
exercise_df['local_start_time'] = pd.to_datetime(exercise_df['local_start_time'])
exercise_df['local_end_time'] = pd.to_datetime(exercise_df['local_end_time'])

#add time zone float to heart_df
def to_float(x):
    return float(x[1])/100
exercise_df['hr_offset'] = exercise_df['time_offset'].str.split('UTC').apply(to_float)

exercise_plot_types = {
	'Histogram': ['Exercise Type'],
	'Scatter': ['Mean Heart Rate vs Time', 'Time Offset vs Time'],
	'Boxplot': ['Duration vs Type', 'Time vs Weekday'],
}

exercise_page = html.Div([
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
		html.H1('Exercise Analysis'),
		html.Div([
			html.H3("Preparing the data sets:"),
			html.P(["One of the data sets produced by the Samsung Health App is a record of the user's exercise. The values retained for this analysis are: ", html.Br(),
				"	- the start time and end time of recording (in UTC date-time format),", html.Br(),
				"	- the user's UTC time zone offset at the time of recording,", html.Br(),
				"	- the device ID (tracking which device recorded the data),", html.Br(),
				"	- a series exercise dependent values (e.g. exercise type, repetition count, distance, speed, heart rate, etc).", html.Br(), 
				"The additional values recorded in the data which were removed for the analysis, because they either contained no new or useful information, \
					(and reason for removal) are:", html.Br(),
				"	- creation time & update time (provide no revelant information that is not already provided by the start & end time values),", html.Br(),
				"	- location & live data (pointers to external json files which weren't present),", html.Br(),
				"	- unique enrty ID (integer index used instead),", html.Br(), 
				"	- app internal package name (same for all entries; main use for developer purposes),", html.Br(), 
				"	- comment, custom, additional, custom exercise type, max rpm, mean rpm, max power, mean power, max caloricburn rate & mean caloricburn rate \
						(all values are empty for each entry),", html.Br(),
				"Since for this data set we're looking at the user's fitness activity we'll also filter out all entries that correspond to casual walking since \
					walking could easily be picked up as an exercise by the app even when it's really not (which will skew the results we see). The chosen critera \
					for a walking entry to be considered exercise are that the activity needs to have an average speed of at least 1.5 m/s to ensure a hightened \
					heart rate, and a minimum duration of 10 minutes. After removal of the mentioned values and entries, the given start and end times (initially \
					recorded in date-time UTC) were converted to a date-time format localized to the user based on the recorded UTC time zone offset (which also \
					takes into account daylight savings time observed during a certain period of the year).", html.Br(), html.Br(), html.Br(),
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			html.H3("Results"),
			html.Br(),
			html.Div([
				dcc.Dropdown(
					id='exercise_plot_type',
					options=[{'label':i, 'value':i} for i in exercise_plot_types.keys()],
					placeholder='Select plot type',
					value='Histogram',
				),
				dcc.Dropdown(
					id='exercise_plot_data',
					placeholder='Select data to plot',
					value='Exercise Type',
				),
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			dcc.Graph(
				id='exercise_graphic',
			),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			html.Br(),
			html.P(["Grouping the data by the user's time zone and graphing the distribution of the exercise type it's clear the the user engaging mostly in custom exercises \
					that are not predefined in the Samsung app documentation (it's possible the the exercise is predefined but the device is misjuding the movements and unsure \
					of the type and just assigning it a custom type). After that follow swimming, walking, running, cycling, and then hiking and elliptical. The user seems to go \
					running and cycling regardless of where they are, and has only gone hiking once whilst travelling.", html.Br(),
				"A scatter plot of the users average heart rate during each logged activity shows that the app is failing to measure a heart rate for a large number of entries. For \
					those which are measured the average heart rate 120bpm during the custom exercise and 160bpm when running.",html.Br(),
				"Plotting the duration of the exercises per type shows that that user spends longest on the custom exercises and only runs or cycles for an average of 25 minutes. This \
					suggest that exercise is not for training purposes but rather a pasttime taken on in a easy going fashion.", html.Br(),
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),

	], id='exercise_analysis'),
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
	Output('exercise_plot_data', 'options'),
	[Input('exercise_plot_type', 'value')])
def set_exercise_plot_data(selected_plot):
	return [{'label':i, 'value':i} for i in exercise_plot_types[selected_plot]]

#update the displayed graph depending on dropdown value
@app.callback(
    Output('exercise_graphic', 'figure'),
    [Input('exercise_plot_data', 'value')])
def update_exercise_plot(plot):
	#histograms
	if plot == 'Exercise Type':
		return {
			'data': [go.Histogram(
					x = exercise_df[exercise_df['time_offset'] == 'UTC-0800']['exercise_type'],
					name = 'UTC-0800',
				),
				go.Histogram(
					x = exercise_df[exercise_df['time_offset'] == 'UTC-0700']['exercise_type'],
					name = 'UTC-0700',
				),
				go.Histogram(
					x = exercise_df[exercise_df['time_offset'] == 'UTC-0500']['exercise_type'],
					name = 'UTC-0500',
				),
				go.Histogram(
					x = exercise_df[exercise_df['time_offset'] == 'UTC-0400']['exercise_type'],
					name = 'UTC-0400',
				),
				go.Histogram(
					x = exercise_df[exercise_df['time_offset'] == 'UTC+0200']['exercise_type'],
					name = 'UTC+0200',
				),
			],
			'layout': go.Layout(
				title = 'Exercise Type Distribution',
				xaxis = {'title': 'Exercise Type'},
				yaxis = {'title': 'Frequency'},
				barmode='stack',
				hovermode = 'closest'
			)
		}
	
	#scatter plot
	if plot == 'Time Offset vs Time':
		chron_sort_df = exercise_df.sort_values(by='local_start_time', axis=0, ascending=True)
		return {
			'data': [go.Scatter(
					x = chron_sort_df[chron_sort_df['exercise_type'] == 'custom']['local_start_time'],
					y = chron_sort_df[chron_sort_df['exercise_type'] == 'custom']['hr_offset'],
					name = 'custom',
					mode = 'markers',
				),
				go.Scatter(
					x = chron_sort_df[chron_sort_df['exercise_type'] == 'walking']['local_start_time'],
					y = chron_sort_df[chron_sort_df['exercise_type'] == 'walking']['hr_offset'],
					name = 'walking',
					mode = 'markers',
				),
				go.Scatter(
					x = chron_sort_df[chron_sort_df['exercise_type'] == 'running']['local_start_time'],
					y = chron_sort_df[chron_sort_df['exercise_type'] == 'running']['hr_offset'],
					name = 'running',
					mode = 'markers',
				),
				go.Scatter(
					x = chron_sort_df[chron_sort_df['exercise_type'] == 'hiking']['local_start_time'],
					y = chron_sort_df[chron_sort_df['exercise_type'] == 'hiking']['hr_offset'],
					name = 'hiking',
					mode = 'markers',
				),
				go.Scatter(
					x = chron_sort_df[chron_sort_df['exercise_type'] == 'swimming']['local_start_time'],
					y = chron_sort_df[chron_sort_df['exercise_type'] == 'swimming']['hr_offset'],
					name = 'swimming',
					mode = 'markers',
				),
				go.Scatter(
					x = chron_sort_df[chron_sort_df['exercise_type'] == 'cycling']['local_start_time'],
					y = chron_sort_df[chron_sort_df['exercise_type'] == 'cycling']['hr_offset'],
					name = 'cycling',
					mode = 'markers',
				),
				go.Scatter(
					x = chron_sort_df[chron_sort_df['exercise_type'] == 'elliptical']['local_start_time'],
					y = chron_sort_df[chron_sort_df['exercise_type'] == 'elliptical']['hr_offset'],
					name = 'elliptical',
					mode = 'markers',
				),
			],
			'layout': go.Layout(
				title = 'Time Zone over Time',
				xaxis = {'title': 'Time (year)'},
				yaxis = {'title': 'Time Zone (UTC)'},
				hovermode = 'closest'
			)
		}
	elif plot == 'Mean Heart Rate vs Time':
		return {
			'data': [go.Scatter(
					x = exercise_df[exercise_df['exercise_type'] == 'custom']['local_start_time'],
					y = exercise_df[exercise_df['exercise_type'] == 'custom']['mean_heart_rate'],
					name = 'custom',
					mode = 'markers',
				),
				go.Scatter(
					x = exercise_df[exercise_df['exercise_type'] == 'walking']['local_start_time'],
					y = exercise_df[exercise_df['exercise_type'] == 'walking']['mean_heart_rate'],
					name = 'walking',
					mode = 'markers',
				),
				go.Scatter(
					x = exercise_df[exercise_df['exercise_type'] == 'running']['local_start_time'],
					y = exercise_df[exercise_df['exercise_type'] == 'running']['mean_heart_rate'],
					name = 'running',
					mode = 'markers',
				),
				go.Scatter(
					x = exercise_df[exercise_df['exercise_type'] == 'hiking']['local_start_time'],
					y = exercise_df[exercise_df['exercise_type'] == 'hiking']['mean_heart_rate'],
					name = 'hiking',
					mode = 'markers',
				),
				go.Scatter(
					x = exercise_df[exercise_df['exercise_type'] == 'swimming']['local_start_time'],
					y = exercise_df[exercise_df['exercise_type'] == 'swimming']['mean_heart_rate'],
					name = 'swimming',
					mode = 'markers',
				),
				go.Scatter(
					x = exercise_df[exercise_df['exercise_type'] == 'cycling']['local_start_time'],
					y = exercise_df[exercise_df['exercise_type'] == 'cycling']['mean_heart_rate'],
					name = 'cycling',
					mode = 'markers',
				),
				go.Scatter(
					x = exercise_df[exercise_df['exercise_type'] == 'elliptical']['local_start_time'],
					y = exercise_df[exercise_df['exercise_type'] == 'elliptical']['mean_heart_rate'],
					name = 'elliptical',
					mode = 'markers',
				),
			],
			'layout': go.Layout(
				title = 'Mean Heart Rate per Exercise Type over Time',
				xaxis = {'title': 'Time (year)'},
				yaxis = {'title': 'Mean Heart Rate (bpm)'},
				hovermode = 'closest'
			)
		}
	
	#boxplots
	if plot == 'Duration vs Type':
		return {
			'data': [go.Box(
					y = exercise_df[exercise_df['exercise_type'] == 'custom']['duration'],
					name = 'custom',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = exercise_df[exercise_df['exercise_type'] == 'walking']['duration'],
					name = 'walking',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = exercise_df[exercise_df['exercise_type'] == 'running']['duration'],
					name = 'running',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = exercise_df[exercise_df['exercise_type'] == 'hiking']['duration'],
					name = 'hiking',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = exercise_df[exercise_df['exercise_type'] == 'swimming']['duration'],
					name = 'swimming',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = exercise_df[exercise_df['exercise_type'] == 'cycling']['duration'],
					name = 'cycling',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = exercise_df[exercise_df['exercise_type'] == 'elliptical']['duration'],
					name = 'elliptical',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
			],
			'layout': go.Layout(
				title = 'Duration per Exercise',
				xaxis = {'title': 'Exercise Type'},
				yaxis = {'title': 'Duration (mins)'},
				hovermode = 'closest'
			)
		}
	elif plot == 'Time vs Weekday':
		return {
			'data': [go.Box(
					y = exercise_df[exercise_df['local_start_time'].dt.dayofweek == 0]['local_start_time'].dt.hour,
					name = 'Monday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = exercise_df[exercise_df['local_start_time'].dt.dayofweek == 1]['local_start_time'].dt.hour,
					name = 'Tuesday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = exercise_df[exercise_df['local_start_time'].dt.dayofweek == 2]['local_start_time'].dt.hour,
					name = 'Wednesday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = exercise_df[exercise_df['local_start_time'].dt.dayofweek == 3]['local_start_time'].dt.hour,
					name = 'Thursday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = exercise_df[exercise_df['local_start_time'].dt.dayofweek == 4]['local_start_time'].dt.hour,
					name = 'Friday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = exercise_df[exercise_df['local_start_time'].dt.dayofweek == 5]['local_start_time'].dt.hour,
					name = 'Saturday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = exercise_df[exercise_df['local_start_time'].dt.dayofweek == 6]['local_start_time'].dt.hour,
					name = 'Sunday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
			],
			'layout': go.Layout(
				title = 'Time of Day of Exercises per Weekday',
				xaxis = {'title': 'Weekday'},
				yaxis = {'title': 'Time of Day (hrs)'},
				hovermode = 'closest'
			)
		}
