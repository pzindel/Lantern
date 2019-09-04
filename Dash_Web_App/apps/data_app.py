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

#import data files
#daily_df = pd.read_csv("cleaned_data/daily_aggregated.csv", sep=',', index_col=0)
exercise_df = pd.read_csv("cleaned_data/exercise_cleaned.csv", sep=',', index_col=0)
floors_df = pd.read_csv("cleaned_data/floors_climbed_cleaned.csv", sep=',', index_col=0)
heart_rate_df = pd.read_csv("cleaned_data/heart_rate_cleaned.csv", sep=',', index_col=0)
sleep_df = pd.read_csv("cleaned_data/sleep_cleaned.csv", sep=',', index_col=0)
step_count_df = pd.read_csv("cleaned_data/step_count_cleaned.csv", sep=',', index_col=0)
summary_df = pd.read_csv("cleaned_data/summary_cleaned.csv", sep=',', index_col=0)

data_page = html.Div([
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
	dcc.Tabs(children=[
			dcc.Tab(label='Sleep Data', value='sleep_set'),
			dcc.Tab(label='Step Count Data', value='step_set'),
			dcc.Tab(label='Floors Climbed Data', value='floors_set'),
			dcc.Tab(label='Heart Rate Data', value='heart_set'),
			dcc.Tab(label='Exercise Data', value='exercise_set'),
			dcc.Tab(label='Summary Data', value='summary_set'),
		], id='data_tabs', value='sleep_set',
	),
	html.Div(id='tabs_content'),
	html.Br(),
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

@app.callback(
	Output('tabs_content', 'children'),
	[Input('data_tabs', 'value')])
def render_table(tab):
	if tab == 'sleep_set':
		return html.Div([
			html.H1('Sleep Data'),
			dash_table.DataTable(
				id='table', 
				columns=[{'name':i, 'id':i} for i in sleep_df.columns],
				data=sleep_df.to_dict('records'),
				n_fixed_rows=1,
				sorting=True,
				pagination_mode="fe",
				pagination_settings={
					"current_page": 0,
					"page_size": 50,
				},
				style_table={'overflowX': 'scroll'},
				style_cell={
					'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
					'whiteSpace': 'normal'
				},
				css=[{
					'selector': '.dash-cell div.dash-cell-value',
					'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
				}],
			)
		], id='sleep'),
	elif tab == 'step_set':
		return html.Div([
			html.H1('Step Data'),
			dash_table.DataTable(
				id='table', 
				columns=[{'name':i, 'id':i} for i in step_count_df.columns],
				data=step_count_df.to_dict('records'),
				n_fixed_rows=1,
				sorting=True,
				pagination_mode="fe",
				pagination_settings={
					"current_page": 0,
					"page_size": 50,
				},
				style_table={'overflowX': 'scroll'},
				style_cell={
					'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
					'whiteSpace': 'normal'
				},
				css=[{
					'selector': '.dash-cell div.dash-cell-value',
					'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
				}],
			)
		], id='step'),
	elif tab == 'floors_set':
		return html.Div([
			html.H1('Floors Climbed Data'),
			dash_table.DataTable(
				id='table', 
				columns=[{'name':i, 'id':i} for i in floors_df.columns],
				data=floors_df.to_dict('records'),
				n_fixed_rows=1,
				sorting=True,
				pagination_mode="fe",
				pagination_settings={
					"current_page": 0,
					"page_size": 50,
				},
				style_table={'overflowX': 'scroll'},
				style_cell={
					'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
					'whiteSpace': 'normal'
				},
				css=[{
					'selector': '.dash-cell div.dash-cell-value',
					'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
				}],
			)
		], id='floors'),
	elif tab == 'heart_set':
		return html.Div([
			html.H1('Heart Rate Data'),
			dash_table.DataTable(
				id='table', 
				columns=[{'name':i, 'id':i} for i in heart_rate_df.columns],
				data=heart_rate_df.to_dict('records'),
				n_fixed_rows=1,
				sorting=True,
				pagination_mode="fe",
				pagination_settings={
					"current_page": 0,
					"page_size": 50,
				},
				style_table={'overflowX': 'scroll'},
				style_cell={
					'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
					'whiteSpace': 'normal'
				},
				css=[{
					'selector': '.dash-cell div.dash-cell-value',
					'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
				}],
			)
		], id='heart'),
	elif tab == 'exercise_set':
		return html.Div([
			html.H1('Exercise Data'),
			dash_table.DataTable(
				id='table', 
				columns=[{'name':i, 'id':i} for i in exercise_df.columns],
				data=exercise_df.to_dict('records'),
				n_fixed_rows=1,
				sorting=True,
				pagination_mode="fe",
				pagination_settings={
					"current_page": 0,
					"page_size": 50,
				},
				style_table={'overflowX': 'scroll'},
				style_cell={
					'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
					'whiteSpace': 'normal'
				},
				css=[{
					'selector': '.dash-cell div.dash-cell-value',
					'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
				}],
			)
		], id='exercise'),
	elif tab == 'summary_set':
		return html.Div([
			html.H1('Summary Data'),
			dash_table.DataTable(
				id='table', 
				columns=[{'name':i, 'id':i} for i in summary_df.columns],
				data=summary_df.to_dict('records'),
				n_fixed_rows=1,
				sorting=True,
				pagination_mode="fe",
				pagination_settings={
					"current_page": 0,
					"page_size": 50,
				},
				style_table={'overflowX': 'scroll'},
				style_cell={
					'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
					'whiteSpace': 'normal'
				},
				css=[{
					'selector': '.dash-cell div.dash-cell-value',
					'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
				}],
			)
		], id='summary'),
