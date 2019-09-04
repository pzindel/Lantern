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
summary_df = pd.read_csv("cleaned_data/summary_cleaned.csv", sep=',', index_col=0)
daily_df = pd.read_csv("cleaned_data/daily_aggregated.csv", sep=',', index_col=0)

#cast to datetime object
summary_df['day_time'] = pd.to_datetime(summary_df['day_time'], unit='ms')
summary_df['run_time'] = pd.to_datetime(summary_df['run_time'], unit='ms').dt.time
summary_df['longest_idle_time'] = pd.to_datetime(summary_df['longest_idle_time'], unit='ms').dt.time
summary_df['longest_active_time'] = pd.to_datetime(summary_df['longest_active_time'], unit='ms').dt.time
summary_df['walk_time'] = pd.to_datetime(summary_df['walk_time'], unit='ms').dt.time
summary_df['others_time'] = pd.to_datetime(summary_df['others_time'], unit='ms').dt.time
summary_df['active_time'] = pd.to_datetime(summary_df['active_time'], unit='ms').dt.time
#cast to datetime object
daily_df['date'] = pd.to_datetime(daily_df['date'])


summary_plot_types = {
	'Scatter': ['Step Count vs Date', 'Distance vs Date', 'Calorie vs Date'],
}

daily_plot_types = {
	'Scatter': ['Step Count vs Date', 'Distance vs Date', 'Calorie vs Date'],
}

aggregated_page = html.Div([
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
		html.H1('Daily Aggregated Analysis'),
		html.Div([
			html.H3("Preparing the data sets:"),
			html.P(["One of the data sets produced by the Samsung Health App is a summary file that records the user's daily activity. The values removed for the \
				analysis, because they either contained no new or useful information are:", html.Br(),
				"	- unique enrty ID (integer index used instead),", html.Br(), 
				"	- app internal package name (same for all entries; main use for developer purposes),", html.Br(), 
				"	- extra_data (pointer to external json files which weren't present),", html.Br(),				
				"After removal of the mentioned values, two entries which contained no data (marked with an longest_idle_time of -1) were also removed.", html.Br(), html.Br(), html.Br(),
			]),
			html.P(["Additionally, we computed a daily aggregated data set using the other provided data sets and applying the most appropriate aggregation function for each value, \
					and then merging the sets together.",
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			html.H3("Results"),
			html.Br(),
			html.H6("Summary data provided by health app:"),
			html.Div([
				dcc.Dropdown(
					id='summary_plot_type',
					options=[{'label':i, 'value':i} for i in summary_plot_types.keys()],
					placeholder='Select plot type',
					value='Scatter',
				),
				dcc.Dropdown(
					id='summary_plot_data',
					placeholder='Select data to plot',
					value='Step Count vs Date',
				),
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			dcc.Graph(
				id='summary_graphic',
			),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			html.Br(),
			html.H6("Daily aggregated data computed from other data sets:"),
			html.Div([
				dcc.Dropdown(
					id='daily_plot_type',
					options=[{'label':i, 'value':i} for i in daily_plot_types.keys()],
					placeholder='Select plot type',
					value='Scatter',
				),
				dcc.Dropdown(
					id='daily_plot_data',
					placeholder='Select data to plot',
					value='Step Count vs Date',
				),
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			dcc.Graph(
				id='daily_graphic',
			),
		], style={'padding-left':'8%', 'padding-right':'8%'}),
		html.Div([
			html.Br(),
			html.P(["Using the app created summary and our computed daily aggregated we can compare the contents of the two for the entries for which they share common values. \
					Here I've chosen to graph the step counts over time, the distance over time, and the calories burned over time. From this we see that the data set provided \
					for the step count data is much shorter than that of the exercise data; the former contain December 2018 data and the latter spans the entire 2018 year. \
					Furthermore, the summary data set spans from June 2016 to January 2019 and thus contains a 2.5 times longer time series. Now comparing the datapoints of each \
					we see that the summary set contains a higher density of data points thus for the calorie and distance plots it seems we are missing points and the points that \
					are present in our computed set are lower than expected. This might be because we are missing and additional dataset that wasn't provided or perhaps between the \
					device logging the data and analyzing it here some data was filtered out and lost along the way. However, if we zoom into the step count plot we see that the few \
					weeks for which the data sets overlap they are roughly the same.", html.Br(),
				"Noticable, just looking at the summary data set, we see an increase in activity in the step count plot starting around January 2018. The last year of data seems \
					to contain fewer daily entries with low step counts, suggesting that the user may have set a goal to be more active in the new year and managed to follow through."
			]),
		], style={'padding-left':'8%', 'padding-right':'8%'}),

	], id='aggregated_analysis'),
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
	Output('summary_plot_data', 'options'),
	[Input('summary_plot_type', 'value')])
def set_summary_plot_data(selected_plot):
	return [{'label':i, 'value':i} for i in summary_plot_types[selected_plot]]

#update the displayed graph depending on dropdown value
@app.callback(
    Output('summary_graphic', 'figure'),
    [Input('summary_plot_data', 'value')])
def update_summary_plot(plot):
	#scatter plot
	if plot == 'Step Count vs Date':
		return {
			'data': [go.Scatter(
				x = summary_df['day_time'],
				y = summary_df['step_count'],
				name = plot,
				mode = 'markers',
			)],
			'layout': go.Layout(
				title = 'Daily Step Count over Time',
				xaxis = {'title': 'Time (date)'},
				yaxis = {'title': 'Step Count'},
				hovermode = 'closest'
			)
		}
	elif plot == 'Distance vs Date':
		return {
			'data': [go.Scatter(
				x = summary_df['day_time'],
				y = summary_df['distance'],
				name = 'distance during exercise',
				mode = 'markers',
			)],
			'layout': go.Layout(
				title = 'Daily Distance over Time',
				xaxis = {'title': 'Time (date)'},
				yaxis = {'title': 'Distance (m)'},
				hovermode = 'closest'
			)
		}
	elif plot == 'Calorie vs Date':
		return {
			'data': [go.Scatter(
				x = summary_df['day_time'],
				y = summary_df['calorie'],
				name = 'calories burned',
				mode = 'markers',
			)],
			'layout': go.Layout(
				title = 'Daily Calorie Burn over Time',
				xaxis = {'title': 'Time (date)'},
				yaxis = {'title': 'Calories (kCal)'},
				hovermode = 'closest'
			)
		}
		
#update the dropdown options depending on the selected graph type
@app.callback(
	Output('daily_plot_data', 'options'),
	[Input('daily_plot_type', 'value')])
def set_daily_plot_data(selected_plot):
	return [{'label':i, 'value':i} for i in daily_plot_types[selected_plot]]

#update the displayed graph depending on dropdown value
@app.callback(
    Output('daily_graphic', 'figure'),
    [Input('daily_plot_data', 'value')])
def update_daily_plot(plot):
	#scatter plot
	if plot == 'Step Count vs Date':
		return {
			'data': [go.Scatter(
				x = daily_df['date'],
				y = daily_df['total_step_count'],
				name = plot,
				mode = 'markers',
			)],
			'layout': go.Layout(
				title = 'Daily Step Count over Time',
				xaxis = {'title': 'Time (date)'},
				yaxis = {'title': 'Step Count'},
				hovermode = 'closest'
			)
		}
	elif plot == 'Distance vs Date':
		return {
			'data': [go.Scatter(
				x = daily_df['date'],
				y = daily_df['total_exercises_distance'],
				name = 'distance during exercise',
				mode = 'markers',
			),
			go.Scatter(
				x = daily_df['date'],
				y = daily_df['total_step_distance'],
				name = 'distance from step count',
				mode = 'markers',
			)],
			'layout': go.Layout(
				title = 'Daily Distance over Time',
				xaxis = {'title': 'Time (date)'},
				yaxis = {'title': 'Distance (m)'},
				hovermode = 'closest'
			)
		}
	elif plot == 'Calorie vs Date':
		return {
			'data': [go.Scatter(
				x = daily_df['date'],
				y = daily_df['total_exercises_calorie'],
				name = 'calories burned during exercise',
				mode = 'markers',
			),
			go.Scatter(
				x = daily_df['date'],
				y = daily_df['total_step_calorie'],
				name = 'calories burned from step count',
				mode = 'markers',
			)],
			'layout': go.Layout(
				title = 'Daily Calorie Burn over Time',
				xaxis = {'title': 'Time (date)'},
				yaxis = {'title': 'Calories (kCal)'},
				hovermode = 'closest'
			)
		}
