import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.linear_model import SGDRegressor

PATH_TO_CSV = "turnstile_weather_v2.csv"

def normalize_features(features):
  ''' 
  Returns the means and standard deviations of the given features, along with a normalized feature
  matrix.
  ''' 
  means = np.mean(features, axis=0)
  std_devs = np.std(features, axis=0)
  normalized_features = (features - means) / std_devs
  return means, std_devs, normalized_features

def recover_params(means, std_devs, norm_intercept, norm_params):
  ''' 
  Recovers the weights for a linear model given parameters that were fitted using
  normalized features. Takes the means and standard deviations of the original
  features, along with the intercept and parameters computed using the normalized
  features, and returns the intercept and parameters that correspond to the original
  features.
  ''' 
  intercept = norm_intercept - np.sum(means * norm_params / std_devs)
  params = norm_params / std_devs
  return intercept, params

def linear_regression(features, values):
  y = values
  x = features
  gdr = linear_model.SGDRegressor()
  fit = gdr.fit(x,y)
  params = fit.coef_
  intercept = fit.intercept_
  #print features
  #labels = list(features.columns.values)
  #coef_table = pd.DataFrame({'Label': labels, 'Coefficients':params})
  #print coef_table

  print gdr.score(x,y)
  return intercept, params

def calculate_r_squared(data, predictions):
	data = np.array(map(float,data[~np.isnan(data)]))
	predictions = np.array(map(float, predictions[~np.isnan(predictions)]))

	sq_differences = (data - predictions)**2
	sum_predicted_sq = np.sum(sq_differences)
    
	mean = np.mean(data)
	sq_mean_differences = (data - mean)**2
	sum_mean_sq = np.sum(sq_mean_differences)
    
	r_squared = 1. - sum_predicted_sq / sum_mean_sq
	print "The r-squared value for this specification is {}".format(r_squared)


def access_data(csv_path):
	turnstile_data = pd.read_csv(csv_path)
	# print type(turnstile_data)
	features = turnstile_data[['rain', 'precipi', 'meantempi', 'meanwspdi', 'weekday']]
	dummy_units = pd.get_dummies(turnstile_data['UNIT'], prefix='unit')
	features = features.join(dummy_units)
	hour_dummy = pd.get_dummies(turnstile_data['hour'], prefix='hour')
	features = features.join(hour_dummy)
	conds_dummy = pd.get_dummies(turnstile_data['conds'], prefix='conds')
	features = features.join(conds_dummy)
  
	values = turnstile_data['ENTRIESn_hourly']

	return features, values

def predictions(features, values):
  # Get numpy arrays
	features_array = features.values
	values_array = values.values
  
	means, std_devs, normalized_features_array = normalize_features(features_array)

  # Perform gradient descent
	norm_intercept, norm_params = linear_regression(normalized_features_array, values_array)
  
	intercept, params = recover_params(means, std_devs, norm_intercept, norm_params)
  
	predictions = intercept + np.dot(features_array, params)
  # The following line would be equivalent:
  # predictions = norm_intercept + np.dot(normalized_features_array, norm_params)
	return predictions

features, values = access_data(PATH_TO_CSV)
predictions = predictions(features, values)
calculate_r_squared(values, predictions)




