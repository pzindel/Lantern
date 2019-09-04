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
sleep_df = pd.read_csv("cleaned_data/sleep_cleaned.csv", sep=',', index_col=0)

#cast to datetime object
sleep_df['local_start_time'] = pd.to_datetime(sleep_df['local_start_time'])
sleep_df['local_end_time'] = pd.to_datetime(sleep_df['local_end_time'])
#add new values
sleep_df['duration_hr'] = (sleep_df['local_end_time'] - sleep_df['local_start_time'])/np.timedelta64(1, 'h')
sleep_df['bedtime_hr'] = sleep_df['local_start_time'].dt.hour
sleep_df['date'] = sleep_df['local_start_time'].dt.date

#add time zone float to heart_df
def to_float(x):
    return float(x[1])/100
sleep_df['hr_offset'] = sleep_df['time_offset'].str.split('UTC').apply(to_float)

sleep_plot_types = {
	'Histogram': ['Duration', 'Efficiency', 'Bedtime'],
	'Scatter': ['Duration vs Time', 'Quality vs Duration', 'Efficiency vs Duration', 'Efficiency vs Time'],
	'Line': ['Timeoffset vs Time'],
	'Boxplot': ['Duration vs Weekday'],
}

sleep_page = html.Div([
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
		html.H1('Sleep Analysis'),
		html.Div([
			html.H3("Preparing the data sets:"),
			html.P(["One of the data sets produced by the Samsung Health App is a record of the user's sleep. It logs several useful values for each sleep entry such: ", html.Br(),
				"	- the sleep start time and end time (in UTC millisecond format),", html.Br(),
				"	- the user's UTC time zone offset at the time of recording,", html.Br(),
				"	- the efficiency of the sleep as a percentage of time time asleep over time in bed,", html.Br(),
				"	- the quality of sleep as rated by the user from a scale of 1-5 (NaN if the user does not assign a rating),", html.Br(),
				"	- the device ID (tracking which device recorded the sleep data).", html.Br(), html.Br(),
				"The original data set also contains a series of additional values which were removed for the analysis because they either contained no new or useful information \
					with regards to this analysis. The values removed (and reason for removal) are:", html.Br(),
				"	- creation time & update time (merely useful for distinguishing between entries that were manually created by the user),", html.Br(),
				"	- unique enrty ID (integer index used instead),", html.Br(), 
				"	- app internal package name (same for all entries; main use for developer purposes),", html.Br(), 
				"	- extra_data (pointer to external json files which weren't present),", html.Br(),
				"	- has_sleep_data (indicator of if the entry was manually logged by user; matches same information as deviceuuid where manually logged entries were created by \
				'jQfnryI8/B' and automatically logged entries were created by 'F/D7+hL5E5'),", html.Br(),
				"	- comment & custom (both values are empty for each entry),", html.Br(),
				"	- original bed time, original wakeup time & original efficiency (all present only for manually logged entries and entries that were edited/rated; in this case \
				the values contain the same information as those mentioned above).", html.Br(), html.Br(),
				"After removal of the mentioned values, entries that occured within an hour of each other (the end of one and start of another) were combined into a single entry  \
					containing an updated start & end time along with a new efficiency that takes into account the previous efficiencies and the wake period in between. \
					Then the given start and end times (initially recorded in milliseconds UTC) were converted to a standard date-time format localized to the user based on the recorded \
					UTC time zone offset (which also takes into account daylight savings time observed during a certain period of the year).", html.Br(), html.Br(), html.Br(),
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			html.H3("Results"),
			html.Br(),
			html.Div([
				dcc.Dropdown(
					id='sleep_plot_type',
					options=[{'label':i, 'value':i} for i in sleep_plot_types.keys()],
					placeholder='Select plot type',
					value='Histogram',
				),
				dcc.Dropdown(
					id='sleep_plot_data',
					placeholder='Select data to plot',
					value='Duration',
				),
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			dcc.Graph(
				id='sleep_graphic',
			),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			html.Br(),
			html.P(["We can begin by looking at a distribution of the duration (in hours) of the sleep entries in the data set. It shows that the user's bulk number of hours \
					slept is centered around 7.5 hours. Additionally, even accounting for sleep entries that occur within an hour of each other there are still a number of \
					entries corresponding to only a couple of hours of sleep. This could mean the user is occassionally getting very little sleep or perhaps taking short naps \
					on days when fewer than the average number of hours are had. Furthermore taking a look the user's time zones placement (select line plot with timeoffset vs time) \
					we can see that the bulk of the entries correspond to when the user is at home (UTC-0400 and UTC-0500 which also account for daylight savings time) and there \
					doesn't seem to be a large difference depending on the time of year in terms of the duration of sleep.", html.Br(), html.Br(),
				"Taking a look at the bedtime hours we can see the user typically goes to sleep close to midnight, with the occassional midday sleep.", html.Br(),
				"The user also experiences high sleep efficiency with an average around 92% suggeting the user has no issues falling asleep majority of the time.", html.Br(),
				"Switching the graph over to a scatter plot of duration over time and efficiency over time we can see the user's sleep patterns over the course of the year for \
					which we have recorded data. At a glance it's clear that the user has very consistent sleep patterns with no particular period being worse than another. \
					Futhermore, exploring the data on the graphs shows that most of the sleep entries with low duration occur within 12 hours of another longer sleep entry. \
					Thus the user is getting sufficient daily sleep.", html.Br(), html.Br(),
				"Exploring the relationships between quantities a bit further we can see that for this case there is no distinguishable correlation between the duration of sleep \
					and the efficiency, nor how the user felt about the sleep and how long it was. In fact, the sleep quality measurement reported by the user may also be influenced \
					by the factor that when the user gets less sleep or bad sleep they may not be in the mood to assign a rating to the sleep entry, thus skewing the metric.", html.Br(), html.Br(),
				"Lastly, I chose to look at how the duration of sleep may differ depending on the day of the week by graphing a series of boxplots. The results again confirm that \
					the users has fairly consistent sleeping patterns. With the exception of a lower average and larger spread on Saturdays, the rest all fall in a range of 7-8 \
					hours per weekday.", html.Br(), html.Br(),
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
	], id='sleep_analysis'),
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
	Output('sleep_plot_data', 'options'),
	[Input('sleep_plot_type', 'value')])
def set_sleep_plot_data(selected_plot):
	return [{'label':i, 'value':i} for i in sleep_plot_types[selected_plot]]
	
#update the displayed graph depending on dropdown value
@app.callback(
    Output('sleep_graphic', 'figure'),
    [Input('sleep_plot_data', 'value')])
def update_sleep_plot(plot):
	#histograms
	if plot == 'Duration':
		return {
			'data': [go.Histogram(
					x = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC-0800')]['duration_hr'],
					name = 'UTC-0800',
				),
				go.Histogram(
					x = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC-0500')]['duration_hr'],
					name = 'UTC-0500',
				),
				go.Histogram(
					x = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC-0400')]['duration_hr'],
					name = 'UTC-0400',
				),
				go.Histogram(
					x = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC+0200')]['duration_hr'],
					name = 'UTC+0200',
				),
			],
			'layout': go.Layout(
				title = 'Sleep Duration Distribution',
				xaxis = {'title': 'Duration (hrs)'},
				yaxis = {'title': 'Frequency'},
				barmode='stack',
				hovermode = 'closest'
			)
		}
	elif plot == 'Efficiency':
		return {
			'data': [go.Histogram(
					x = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC-0800')]['efficiency'],
					name = 'UTC-0800',
				),
				go.Histogram(
					x = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC-0500')]['efficiency'],
					name = 'UTC-0500',
				),
				go.Histogram(
					x = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC-0400')]['efficiency'],
					name = 'UTC-0400',
				),
				go.Histogram(
					 x= sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC+0200')]['efficiency'],
					 name = 'UTC+0200',
				),
			],
			'layout': go.Layout(
				title = 'Sleep Efficiency Distribution',
				xaxis = {'title': 'Efficiency (%)'},
				yaxis = {'title': 'Frequency'},
				barmode='stack',
				hovermode = 'closest'
			)
		}
	elif plot == 'Bedtime':
		return {
			'data': [go.Histogram(
					x = sleep_df[sleep_df['time_offset'] == 'UTC-0800']['bedtime_hr'],
					name = 'UTC-0800',
					nbinsx = 24,
				),
				go.Histogram(
					x = sleep_df[sleep_df['time_offset'] == 'UTC-0500']['bedtime_hr'],
					name = 'UTC-0500',
					nbinsx = 24,
				),
				go.Histogram(
					x = sleep_df[sleep_df['time_offset'] == 'UTC-0400']['bedtime_hr'],
					name = 'UTC-0400',
					nbinsx = 24,
				),
				go.Histogram(
					x = sleep_df[sleep_df['time_offset'] == 'UTC+0200']['bedtime_hr'],
					name = 'UTC+0200',
					nbinsx = 24,
				),
			],
			'layout': go.Layout(
				title = 'Bedtime Hour Distribution',
				xaxis = {'title': 'Bedtime Hour'},
				yaxis = {'title': 'Frequency'},
				barmode='stack',
				hovermode='closest'
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
	elif plot == 'Quality vs Duration':
		return {
			'data': [go.Scatter(
					x = sleep_df[sleep_df['time_offset'] == 'UTC-0800']['duration_hr'],
					y = sleep_df[sleep_df['time_offset'] == 'UTC-0800']['quality']-5e4,
					name = 'UTC-0800',
					mode = 'markers',
				),
				go.Scatter(
					x = sleep_df[sleep_df['time_offset'] == 'UTC-0500']['duration_hr'],
					y = sleep_df[sleep_df['time_offset'] == 'UTC-0500']['quality']-5e4,
					name = 'UTC-0500',
					mode = 'markers',
				),
				go.Scatter(
					x = sleep_df[sleep_df['time_offset'] == 'UTC-0400']['duration_hr'],
					y = sleep_df[sleep_df['time_offset'] == 'UTC-0400']['quality']-5e4,
					name = 'UTC-0400',
					mode = 'markers',
				),
				go.Scatter(
					x = sleep_df[sleep_df['time_offset'] == 'UTC+0200']['duration_hr'],
					y = sleep_df[sleep_df['time_offset'] == 'UTC+0200']['quality']-5e4,
					name = 'UTC+0200',
					mode = 'markers',
				),
			],
			'layout': go.Layout(
				title = 'Sleep Quality vs Duration',
				xaxis = {'title': 'Duration (hrs)'},
				yaxis = {'title': 'Quality (1-5 star rating)'},
				hovermode = 'closest'
			)
		}
	elif plot == 'Efficiency vs Duration':
		return {
			'data': [go.Scatter(
					x = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC-0800')]['duration_hr'],
					y = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC-0800')]['efficiency'],
					name = 'UTC-0800',
					mode = 'markers',
				),
				go.Scatter(
					x = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC-0500')]['duration_hr'],
					y = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC-0500')]['efficiency'],
					name = 'UTC-0500',
					mode = 'markers',
				),
				go.Scatter(
					x = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC-0400')]['duration_hr'],
					y = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC-0400')]['efficiency'],
					name = 'UTC-0400',
					mode = 'markers',
				),
				go.Scatter(
					x = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC+0200')]['duration_hr'],
					y = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC+0200')]['efficiency'],
					name = 'UTC+0200',
					mode = 'markers',
				),
			],
			'layout': go.Layout(
				title = 'Sleep Efficiency vs Duration',
				xaxis = {'title': 'Duration (hrs)'},
				yaxis = {'title': 'Efficiency ((hrs asleep)/(hrs in bed))'},
				hovermode = 'closest'
			)
		}
	elif plot == 'Efficiency vs Time':
		return {
			'data': [go.Scatter(
					x = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC-0800')]['local_start_time'],
					y = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC-0800')]['efficiency'],
					name = 'UTC-0800',
					mode = 'markers',
				),
				go.Scatter(
					x = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC-0500')]['local_start_time'],
					y = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC-0500')]['efficiency'],
					name = 'UTC-0500',
					mode = 'markers',
				),
				go.Scatter(
					x = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC-0400')]['local_start_time'],
					y = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC-0400')]['efficiency'],
					name = 'UTC-0400',
					mode = 'markers',
				),
				go.Scatter(
					x = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC+0200')]['local_start_time'],
					y = sleep_df[(sleep_df['efficiency'] != 0) & (sleep_df['time_offset'] == 'UTC+0200')]['efficiency'],
					name = 'UTC+0200',
					mode = 'markers',
				),
			],
			'layout': go.Layout(
				title = 'Sleep Efficiency over Time',
				xaxis = {'title': 'Time (year)'},
				yaxis = {'title': 'Efficiency ((hrs asleep)/(hrs in bed))'},
				hovermode = 'closest'
			)
		}	
	
	#boxplot
	if plot == 'Duration vs Weekday':
		return {
			'data': [go.Box(
					y = sleep_df[sleep_df['local_start_time'].dt.dayofweek == 0]['duration_hr'],
					name = 'Monday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = sleep_df[sleep_df['local_start_time'].dt.dayofweek == 1]['duration_hr'],
					name = 'Tuesday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = sleep_df[sleep_df['local_start_time'].dt.dayofweek == 2]['duration_hr'],
					name = 'Wednesday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = sleep_df[sleep_df['local_start_time'].dt.dayofweek == 3]['duration_hr'],
					name = 'Thursday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = sleep_df[sleep_df['local_start_time'].dt.dayofweek == 4]['duration_hr'],
					name = 'Friday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = sleep_df[sleep_df['local_start_time'].dt.dayofweek == 5]['duration_hr'],
					name = 'Saturday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
				go.Box(
					y = sleep_df[sleep_df['local_start_time'].dt.dayofweek == 6]['duration_hr'],
					name = 'Sunday',
					boxpoints = 'outliers',
					boxmean = 'sd'
				),
			],
			'layout': go.Layout(
				title = 'Sleep Duration per Weekday',
				xaxis = {'title': 'Weekday'},
				yaxis = {'title': 'Duration (hrs)'},
				hovermode = 'closest'
			)
		}
		
	#line plot
	chron_sort_df = sleep_df.sort_values(by='local_start_time', axis=0, ascending=True)
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
