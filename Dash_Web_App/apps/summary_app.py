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
daily_df = pd.read_csv("cleaned_data/daily_aggregated.csv", sep=',', index_col=0)
exercise_df = pd.read_csv("cleaned_data/exercise_cleaned.csv", sep=',', index_col=0)
floors_df = pd.read_csv("cleaned_data/floors_climbed_cleaned.csv", sep=',', index_col=0)
heart_rate_df = pd.read_csv("cleaned_data/heart_rate_cleaned.csv", sep=',', index_col=0)
sleep_df = pd.read_csv("cleaned_data/sleep_cleaned.csv", sep=',', index_col=0)
step_count_df = pd.read_csv("cleaned_data/step_count_cleaned.csv", sep=',', index_col=0)
summary_df = pd.read_csv("cleaned_data/summary_cleaned.csv", sep=',', index_col=0)

#cast to datetime object
sleep_df['local_start_time'] = pd.to_datetime(sleep_df['local_start_time'])
sleep_df['local_end_time'] = pd.to_datetime(sleep_df['local_end_time'])
step_count_df['local_start_time'] = pd.to_datetime(step_count_df['local_start_time'])
step_count_df['local_end_time'] = pd.to_datetime(step_count_df['local_end_time'])
heart_rate_df['local_start_time'] = pd.to_datetime(heart_rate_df['local_start_time'])
heart_rate_df['local_end_time'] = pd.to_datetime(heart_rate_df['local_end_time'])
floors_df['local_start_time'] = pd.to_datetime(floors_df['local_start_time'])
floors_df['local_end_time'] = pd.to_datetime(floors_df['local_end_time'])
exercise_df['local_start_time'] = pd.to_datetime(exercise_df['local_start_time'])
exercise_df['local_end_time'] = pd.to_datetime(exercise_df['local_end_time'])
summary_df['day_time'] = pd.to_datetime(summary_df['day_time'], unit='ms')
summary_df['run_time'] = pd.to_datetime(summary_df['run_time'], unit='ms').dt.time
summary_df['longest_idle_time'] = pd.to_datetime(summary_df['longest_idle_time'], unit='ms').dt.time
summary_df['longest_active_time'] = pd.to_datetime(summary_df['longest_active_time'], unit='ms').dt.time
summary_df['walk_time'] = pd.to_datetime(summary_df['walk_time'], unit='ms').dt.time
summary_df['others_time'] = pd.to_datetime(summary_df['others_time'], unit='ms').dt.time
summary_df['active_time'] = pd.to_datetime(summary_df['active_time'], unit='ms').dt.time
daily_df['date'] = pd.to_datetime(daily_df['date'])

#add new values to sleep_df
sleep_df['duration_hr'] = (sleep_df['local_end_time'] - sleep_df['local_start_time'])/np.timedelta64(1, 'h')
sleep_df['bedtime_hr'] = sleep_df['local_start_time'].dt.hour
sleep_df['date'] = sleep_df['local_start_time'].dt.date

#add time zone float to heart_df
def to_float(x):
    return float(x[1])/100
heart_rate_df['hr_offset'] = heart_rate_df['time_offset'].str.split('UTC').apply(to_float)

summary_app_plot_types = {
	'Histogram': ['Heart Rate', 'Exercise Type'],
	'Scatter': ['Duration vs Time'],
	'Line': ['Time Offset vs Time'],
}

summary_page = html.Div([
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
		html.H1('Health App Data Analysis'),
		html.Div([
			html.H3("Preparing the data sets:"),
			html.P(["[Refer to other pages to see how each data set was prepared.]", html.Br(), html.Br(), html.Br(),
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			html.H3("Results"),
			html.Br(), 
			html.Div([
				dcc.Dropdown(
					id='summary_app_plot_type',
					options=[{'label':i, 'value':i} for i in summary_app_plot_types.keys()],
					placeholder='Select plot type',
					value='Histogram',
				),
				dcc.Dropdown(
					id='summary_app_plot_data',
					placeholder='Select data to plot',
					value='Heart Rate',
				),
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			dcc.Graph(
				id='summary_app_graphic',
			),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			html.Br(),
			html.P(["To get some insight into the activities of the user that the present data was logged for we can start by looking at the time zone logs for the largest time \
					time series set we have, which happens to be the heart rate records. [Setting the graph above to 'Line' and 'Time Offset vs Time'] we can see that we have records \
					of some of the user's travels over the course of the last two and a half years. The user data starts in June 2016 located in an Eastern-Europe/Middle-Eastern time \
					zone which then promptly shifts to a North America west-coast time zone. The few data points present indicate the user stayed on the west-coast for about 7 months \
					and then moved to the east-coast where they have resided since, and only travelling across timezones for short trips. We note that the +/-1 shifts in timezone over \
					the course of the year correspond to changes in daylight savings time. From this we may conclude that as of the past 20 months the user has resided in roughly \
					the same geographical region.", html.Br(), html.Br(),
				"Next we can take a look at the user's sleeping patterns [by switching the graph to 'Scatter' and 'Duration vs Time']. This plot shows us that over the course of the \
					previous year the user has consisently gotten 7-9 hours of sleep. Zooming in on the data further shows that the user occassionally gets less than 4 hours of sleep \
					but often makes up for it in several naps in one day. This leads us to reason that the user is someone with stable work hours (and by extension stalbe employment) \
					and a proper life balance.", html.Br(), html.Br(),
				"Moving on to the users health, we can plot the users heart rate record of the past years [by selecting 'Histogram' and 'Heart Rate' above]. This displays a heart rate \
					that is firmly distributed around roughly 60 bpm which is considered an indicator of someone who is either still quite young or exercises enough to stay in good \
					shape. To help decide which it may be we can plot the distribution of exercise types from the user's exercise data. The user does quite a bit of swimming, which \
					typically a preferred exercise for aging persons, however the user also cycles and runs which are more high impact exercises. In addition to that looking at the \
					speeds at which the user occassionally runs (not depicted here) idicates that the user is more than likely on the younger side. Based on the user's sleep patterns \
					and travels, along with the exercise and heart rate data we may conclude that the data belongs to an active mid-30 year old with a stable work-life balance.", html.Br(),
			])
		], style={'padding-left':'8%', 'padding-right':'8%'}),
	], id='summary_app_analysis'),
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
	Output('summary_app_plot_data', 'options'),
	[Input('summary_app_plot_type', 'value')])
def set_summary_app_plot_data(selected_plot):
	return [{'label':i, 'value':i} for i in summary_app_plot_types[selected_plot]]
	
#update the displayed graph depending on dropdown value
@app.callback(
    Output('summary_app_graphic', 'figure'),
    [Input('summary_app_plot_data', 'value')])
def update_summary_app_plot(plot):
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
	elif plot == 'Exercise Type':
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

	#scatter plots
	if plot == 'Duration vs Time':
		return {
			'data': [go.Scatter(
					x = sleep_df[sleep_df['time_offset'] == 'UTC-0800']['local_start_time'],
					y = sleep_df[sleep_df['time_offset'] == 'UTC-0800']['duration_hr'],
					name = 'UTC-0800',
					mode = 'markers',
				),
				go.Scatter(
					x = sleep_df[sleep_df['time_offset'] == 'UTC-0500']['local_start_time'],
					y = sleep_df[sleep_df['time_offset'] == 'UTC-0500']['duration_hr'],
					name = 'UTC-0500',
					mode = 'markers',
				),
				go.Scatter(
					x = sleep_df[sleep_df['time_offset'] == 'UTC-0400']['local_start_time'],
					y = sleep_df[sleep_df['time_offset'] == 'UTC-0400']['duration_hr'],
					name = 'UTC-0400',
					mode = 'markers',
				),
				go.Scatter(
					x = sleep_df[sleep_df['time_offset'] == 'UTC+0200']['local_start_time'],
					y = sleep_df[sleep_df['time_offset'] == 'UTC+0200']['duration_hr'],
					name = 'UTC+0200',
					mode = 'markers',
				),
			],
			'layout': go.Layout(
				title = 'Sleep Duration over Time',
				xaxis = {'title': 'Time (year)'},
				yaxis = {'title': 'Duration (hrs)'},
				hovermode = 'closest'
			)
		}