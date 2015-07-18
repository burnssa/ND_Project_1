
import numpy as np
import pandas as pd
import ggplot
from ggplot import *
from pandas import *
import scipy.stats
import string

PATH_TO_CSV = "turnstile_weather_v2.csv"

def run_hourly_entry_chart(csv_path):
	turnstile_data = pd.read_csv(csv_path)

	#Create table melted with hourly entries as values on index of 'hour'
	turnstile_data['hour_float'] = turnstile_data['hour'].astype(float)
	turnstile_data['UNIT_float'] = turnstile_data['UNIT'].str.replace('R','').astype(float)
	turnstile_data['entries_float'] = turnstile_data['ENTRIESn'].str.replace(',','').convert_objects(convert_numeric=True)

	#Get an array of top 10 units of ENTRIESn
	turnstile_data_unit = turnstile_data.groupby(['UNIT_float']).sum()
	turnstile_data_sorted = turnstile_data_unit.sort(['entries_float'], ascending=[0]).reset_index()
	top_10_units = turnstile_data_sorted['UNIT_float'].head(10)
	print top_10_units
	
	top_turnstile_data = turnstile_data[turnstile_data['UNIT_float'].isin(top_10_units)]
	# top 10 UNITs by total entries
	print top_turnstile_data
	
	#put data on top 10 stations in a pviot table with columns indexed on hourly entries
	hourly_table_df = pd.pivot_table(top_turnstile_data,index=['hour_float'], columns=['UNIT_float'], values=['ENTRIESn_hourly'],aggfunc=np.sum).reset_index(0)
	hourly_graph = pd.melt(hourly_table_df, id_vars=['hour_float'])

	print hourly_graph
	
	#print graph
	p = ggplot(hourly_graph, aes(x ='hour_float', y ='value', color='UNIT_float')) +\
	geom_point(alpha = 0.9, size=40) +\
	stat_smooth(colour='red', span=.6) +\
	xlab("Hour of Day") +\
	ylab("Hourly Entries for Preceding Four Hours") +\
	ggtitle("Intra-day Entries at NYC's 10 Largest Subway Units") +\
	xlim(0,20) +\
	ylim(0,800000)
	print p

run_hourly_entry_chart(PATH_TO_CSV)
