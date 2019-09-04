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
step_count_df = pd.read_csv("cleaned_data/step_count_cleaned.csv", sep=',', index_col=0)

#cast to datetime object
step_count_df['local_start_time'] = pd.to_datetime(step_count_df['local_start_time'])
step_count_df['local_end_time'] = pd.to_datetime(step_count_df['local_end_time'])

step_plot_types = {
	'Histogram': ['Step Count', 'Time of Day'],
	'Scatter': ['Count vs Time', 'Count vs Distance', 'Calorie vs Distance'],
	'Boxplot': ['Distance vs Weekday'],
}

step_page = html.Div([
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
		html.H1('Step Count Analysis'),
		html.Div([
			html.H3("Preparing the data sets:"),
			html.P(["One of the data sets produced by the Samsung Health App is a record of the user's steps taken. The values retained for this analysis are: ", html.Br(),
				"	- the start time and end time (in UTC date-time format),", html.Br(),
				"	- the user's UTC time zone offset at the time of recording,", html.Br(),
				"	- a count of the user's steps taken between the given time frame,", html.Br(),
				"	- the calories burn during the exercise (in kilocalories),", html.Br(),
				"	- the speed of the user during the exercise (in meters per second),", html.Br(),
				"	- the distance covered during the exercise (in meters),", html.Br(),
				"	- the poisition, on the user's body, of the device while recording,", html.Br(),
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
					id='step_plot_type',
					options=[{'label':i, 'value':i} for i in step_plot_types.keys()],
					placeholder='Select plot type',
					value='Histogram',
				),
				dcc.Dropdown(
					id='step_plot_data',
					placeholder='Select data to plot',
					value='Step Count',
				),
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			dcc.Graph(
				id='step_graphic',
			),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			html.Br(),
			html.P(["The distribution of the steps counted by the entries is skewed towards a lower number of steps, as one would expect from someone with a more sedentary \
					lifestyle and workplace. Similarly, the distribution of daytime hours when entries are logged is spread across the daylight hours of a typicall day.", html.Br(),
				"Taking a look at a set of boxplots for distance covered per entry every weekday we see similar average and spread regardless of the day of the week. Notably, Friday \
					is the day which contains the fewest number of high distance outliers.", html.Br(), html.Br(),
				"Plotting the step count over time shows that the data set only occurs over the course of 5 weeks and has no discernable change in pattern over that span.", html.Br(),
				"As expected, the step count vs distance plot shows us the approximate linear relationship between the number of steps and the distance covered by the user. Intrestingly, \
					we can colour code the entries with the user's speed to find that the faster the user is travelling the larger the distance covered with fewer step and also the more \
					consistent the correlation is considering that at lower speed a users will easily be able to vary their stride length.", html.Br(),
				"Switching to the calories burned over distance cover, the relation is again nearly linear, however a larger number of slow pace entries show much higher caloric burn \
					than entries where the user ran for larger distances. A difference in terrain covered during the activity might be the reason for the disparity.", html.Br(),
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),

	], id='step_analysis'),
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
	Output('step_plot_data', 'options'),
	[Input('step_plot_type', 'value')])
def set_step_plot_data(selected_plot):
	return [{'label':i, 'value':i} for i in step_plot_types[selected_plot]]
	
#update the displayed graph depending on dropdown value
@app.callback(
    Output('step_graphic', 'figure'),
    [Input('step_plot_data', 'value')])
def update_step_plot(plot):
	#histograms
	if plot == 'Step Count':
		return {
			'data': [go.Histogram(
					x = step_count_df[step_count_df['time_offset'] == 'UTC-0800']['count'],
					name = 'UTC-0800',
				),
				go.Histogram(
					x = step_count_df[step_count_df['time_offset'] == 'UTC-0500']['count'],
					name = 'UTC-0500',
				),
				go.Histogram(
					x = step_count_df[step_count_df['time_offset'] == 'UTC-0400']['count'],
					name = 'UTC-0400',
				),
				go.Histogram(
					x = step_count_df[step_count_df['time_offset'] == 'UTC+0200']['count'],
					name = 'UTC+0200',
				),
			],
			'layout': go.Layout(
				title = 'Step Count Distribution',
				xaxis = {'title': 'Steps'},
				yaxis = {'title': 'Frequency'},
				barmode='stack',
				hovermode = 'closest'
			)
		}
	elif plot == 'Time of Day':
		return {
			'data': [go.Histogram(
					x = step_count_df[step_count_df['speed'] < 1.3]['local_start_time'].dt.hour,
					name = 'slow walk (< 1.3 m/s)',
					nbinsx = 24,
					xbins=dict(
						start = '00:00:00',
						end = '23:59:59',
						size = 'M2'),
					autobinx = False
				),
				go.Histogram(
					x = step_count_df[(step_count_df['speed'] > 1.3) & (step_count_df['speed'] < 2.0)]['local_start_time'].dt.hour,
					name = 'walk (1.3 - 2.0 m/s)',
					nbinsx = 24,
					xbins=dict(
						start = '00:00:00',
						end = '23:59:59',
						size = 'M2'),
					autobinx = False
				),
				go.Histogram(
					x = step_count_df[(step_count_df['speed'] > 2.0) & (step_count_df['speed'] < 2.5)]['local_start_time'].dt.hour,
					name = 'jog (2.0 - 2.5 m/s)',
					nbinsx = 24,
					xbins=dict(
						start = '00:00:00',
						end = '23:59:59',
						size = 'M2'),
					autobinx = False
				),
				go.Histogram(
					x = step_count_df[(step_count_df['speed'] > 2.5) & (step_count_df['speed'] < 3.5)]['local_start_time'].dt.hour,
					name = 'run (2.5 - 3.5 m/s)',
					nbinsx = 24,
					xbins=dict(
						start = '00:00:00',
						end = '23:59:59',
						size = 'M2'),
					autobinx = False
				),
				go.Histogram(
					x = step_count_df[step_count_df['speed'] > 3.5]['local_start_time'].dt.hour,
					name = 'fast run (> 3.5 m/s)',
					nbinsx = 24,
					xbins=dict(
						start = '00:00:00',
						end = '23:59:59',
						size = 'M2'),
					autobinx = False
				),
			],
			'layout': go.Layout(
				title = 'Time of Day Distribution',
				xaxis = {'title': 'Time (hr)'},
				yaxis = {'title': 'Frequency'},
				barmode='stack',
				hovermode = 'closest'
			)
		}
	
	#scatter plots
	if plot == 'Count vs Time':
		return {
			'data': [go.Scatter(
					x = step_count_df['local_start_time'],
					y = step_count_df['count'],
					name = 'UTC-0500',
					mode = 'markers',
				),
			],
			'layout': go.Layout(
				title = 'Step Count over Time',
				xaxis = {'title': 'Time (year)'},
				yaxis = {'title': 'Step Count'},
				hovermode = 'closest'
			)
		}
	elif plot == 'Count vs Distance':
		return {
			'data': [go.Scatter(
					x = step_count_df[step_count_df['speed'] < 1.3]['distance'],
					y = step_count_df[step_count_df['speed'] < 1.3]['count'],
					name = 'slow walk (< 1.3 m/s)',
					mode = 'markers',
				),
				go.Scatter(
					x = step_count_df[(step_count_df['speed'] > 1.3) & (step_count_df['speed'] < 2.0)]['distance'],
					y = step_count_df[(step_count_df['speed'] > 1.3) & (step_count_df['speed'] < 2.0)]['count'],
					name = 'walk (1.3 - 2.0 m/s)',
					mode = 'markers',
				),
				go.Scatter(
					x = step_count_df[(step_count_df['speed'] > 2.0) & (step_count_df['speed'] < 2.5)]['distance'],
					y = step_count_df[(step_count_df['speed'] > 2.0) & (step_count_df['speed'] < 2.5)]['count'],
					name = 'jog (2.0 - 2.5 m/s)',
					mode = 'markers',
				),
				go.Scatter(
					x = step_count_df[(step_count_df['speed'] > 2.5) & (step_count_df['speed'] < 3.5)]['distance'],
					y = step_count_df[(step_count_df['speed'] > 2.5) & (step_count_df['speed'] < 3.5)]['count'],
					name = 'run (2.5 - 3.5 m/s)',
					mode = 'markers',
				),
				go.Scatter(
					x = step_count_df[step_count_df['speed'] > 3.5]['distance'],
					y = step_count_df[step_count_df['speed'] > 3.5]['count'],
					name = 'fast run (> 3.5 m/s)',
					mode = 'markers',
				),
			],
			'layout': go.Layout(
				title = 'Step Count vs Distance',
				xaxis = {'title': 'Distance (m)'},
				yaxis = {'title': 'Step Count'},
				hovermode = 'closest'
			)
		}
	elif plot == 'Calorie vs Distance':
		return {
			'data': [go.Scatter(
					x = step_count_df[step_count_df['speed'] < 1.3]['distance'],
					y = step_count_df[step_count_df['speed'] < 1.3]['calorie'],
					name = 'slow walk (< 1.3 m/s)',
					mode = 'markers',
				),
				go.Scatter(
					x = step_count_df[(step_count_df['speed'] > 1.3) & (step_count_df['speed'] < 2.0)]['distance'],
					y = step_count_df[(step_count_df['speed'] > 1.3) & (step_count_df['speed'] < 2.0)]['calorie'],
					name = 'walk (1.3 - 2.0 m/s)',
					mode = 'markers',
				),
				go.Scatter(
					x = step_count_df[(step_count_df['speed'] > 2.0) & (step_count_df['speed'] < 2.5)]['distance'],
					y = step_count_df[(step_count_df['speed'] > 2.0) & (step_count_df['speed'] < 2.5)]['calorie'],
					name = 'jog (2.0 - 2.5 m/s)',
					mode = 'markers',
				),
				go.Scatter(
					x = step_count_df[(step_count_df['speed'] > 2.5) & (step_count_df['speed'] < 3.5)]['distance'],
					y = step_count_df[(step_count_df['speed'] > 2.5) & (step_count_df['speed'] < 3.5)]['calorie'],
					name = 'run (2.5 - 3.5 m/s)',
					mode = 'markers',
				),
				go.Scatter(
					x = step_count_df[step_count_df['speed'] > 3.5]['distance'],
					y = step_count_df[step_count_df['speed'] > 3.5]['calorie'],
					name = 'fast run (> 3.5 m/s)',
					mode = 'markers',
				),
			],
			'layout': go.Layout(
				title = 'Calories Burned vs Distance',
				xaxis = {'title': 'Distance (m)'},
				yaxis = {'title': 'Calories Burned (kcalories)'},
				hovermode = 'closest'
			)
		}
	
	#boxplots
	if plot == 'Distance vs Weekday':
		return {
			'data': [go.Box(
					y = step_count_df[step_count_df['local_start_time'].dt.dayofweek == 0]['distance'],
					name = 'Monday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = step_count_df[step_count_df['local_start_time'].dt.dayofweek == 1]['distance'],
					name = 'Tuesday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = step_count_df[step_count_df['local_start_time'].dt.dayofweek == 2]['distance'],
					name = 'Wednesday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = step_count_df[step_count_df['local_start_time'].dt.dayofweek == 3]['distance'],
					name = 'Thursday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = step_count_df[step_count_df['local_start_time'].dt.dayofweek == 4]['distance'],
					name = 'Friday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = step_count_df[step_count_df['local_start_time'].dt.dayofweek == 5]['distance'],
					name = 'Saturday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = step_count_df[step_count_df['local_start_time'].dt.dayofweek == 6]['distance'],
					name = 'Sunday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
			],
			'layout': go.Layout(
				title = 'Distance per Weekday',
				xaxis = {'title': 'Weekday'},
				yaxis = {'title': 'Distance (m)'},
				hovermode = 'closest'
			)
		}
