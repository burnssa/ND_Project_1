
import numpy as np
import pandas as pd
import ggplot
from ggplot import *
from pandas import *
import scipy.stats

PATH_TO_CSV = "turnstile_weather_v2.csv"

def run_hourly_entry_chart(csv_path):
	turnstile_data = pd.read_csv(csv_path)
	#print turnstile_data.describe()

	#Create table melted with hourly entries as values on index of 'hour'
	turnstile_data['hour_float'] = turnstile_data['hour'].astype(float)
	print type(turnstile_data['hour_float'][0])

	turnstile_data['UNIT_float'] = turnstile_data['UNIT'].str.replace('R','').astype(float)
	print type(turnstile_data['hour_float'][0])

	hourly_table_df = pd.pivot_table(turnstile_data,index=['hour_float'], columns=['UNIT_float'], values=['ENTRIESn_hourly'],aggfunc=np.sum).reset_index(0)
	hourly_graph = pd.melt(hourly_table_df, id_vars=['hour_float'])
	print hourly_graph

	# print hourly_graph
	p = ggplot(hourly_graph, aes(x ='hour_float', y ='value', color='UNIT_float')) +\
	geom_line(alpha = 0.6, size=5) +\
	xlab("Hour of Day") +\
	ylab("Hourly Entries for Preceding Four Hours")
	print p

run_hourly_entry_chart(PATH_TO_CSV)
