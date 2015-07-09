import numpy as np
import pandas as pd
import ggplot
from ggplot import *
import scipy.stats

PATH_TO_CSV = "turnstile_weather_v2.csv"

def print_histogram(csv_path):
  turnstile_data = pd.read_csv(PATH_TO_CSV)
  print turnstile_data.describe()

  #Create rainy_day hourly entries column
  turnstile_data['rainy_entries'] = turnstile_data[turnstile_data['rain']==1]['ENTRIESn_hourly']
  turnstile_data['non_rainy_entries'] = turnstile_data[turnstile_data['rain']==0]['ENTRIESn_hourly']
  print turnstile_data['rainy_entries'].describe()
  print turnstile_data['non_rainy_entries'].describe()

  rain_graph_df = pd.melt(turnstile_data, id_vars=['datetime'], value_vars=['rainy_entries', 'non_rainy_entries']).dropna().reset_index()

  #create probability density faceted chart for rainy and non-rainy days
  p = ggplot(rain_graph_df, aes(x='value', color= 'variable', fill='variable')) +\
  geom_histogram(alpha = 0.3, binwidth=50) +\
  scale_x_continuous(limits=(0,10000)) +\
  xlab("Hourly Entry Probability Density on Rainy and Non-Rainy Days")
  print p
  
  # #Run MannWhitney test with original rain / non-rain columns
  non_rainy_entries = turnstile_data['non_rainy_entries'].dropna()
  rainy_entries = turnstile_data['rainy_entries'].dropna()
  print non_rainy_entries.describe()
  print rainy_entries.describe()

  results = scipy.stats.mannwhitneyu(non_rainy_entries, rainy_entries, False)
  print results

  # # print rain_dummy
  # print p
  #print turnstile_data

#def calculate_mw_test()

print_histogram(PATH_TO_CSV)
	#calculate_mw_test(sample1, sample2)

   
    