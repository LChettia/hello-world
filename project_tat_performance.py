import pandas as pd
# from pandas.tseries.offsets import *
import datetime
import numpy as np



# print('Being files import...')
#import intake csv file
df_intake = pd.read_csv("intake_data.csv", parse_dates=["intake_date"])
#check for duplicate intake dates in the file
duplicate_intake_dates = df_intake[df_intake.duplicated(['intake_date'], keep=False)]
duplicate_intake_dates_count = duplicate_intake_dates['intake_date'].count()

#import output csv
df_output = pd.read_csv("output_data.csv", parse_dates=["output_date"])
#check for duplicate output dates in the file
duplicate_output_dates = df_output[df_output.duplicated(['output_date'], keep=False)]
duplicate_output_dates_count = duplicate_output_dates['output_date'].count()
#give warning for duplicates and exit
if duplicate_output_dates_count > 0:
	print('Duplicate details of output date as below, please correct the details in the output file and try again!')
	print(duplicate_output_dates, "\n")
#give warning for duplicates and exit
elif duplicate_intake_dates_count > 0:
	print('Duplicate details of intake date as below, please correct the details in the intake file and try again!')
	print(duplicate_intake_dates, "\n")
else:
	# print('File import sucessful!!')
	# print(df_intake, "\n")
	# print(df_output, "\n")


	df_intake['intake_balance'] = df_intake['intake_count']
	df_output['output_balance'] = df_output['output_count']
	#method to get current intake date to plot
	min_intake_date = df_intake[df_intake['intake_balance']>0]['intake_date'].min()
	#method to get the corresponding intake count of the current intake date to plot
	min_intake_date_value = df_intake[df_intake['intake_date']==min_intake_date]['intake_balance'].min()
	#method to get current output date to plot
	min_output_date = df_output[(df_output['output_balance'] > 0) & (df_output['output_date'] >= min_intake_date)]['output_date'].min()
	#method to get the corresponding output count of the current output date to plot 
	min_output_date_value = df_output[df_output['output_date']==min_output_date]['output_balance'].min()

	#empty dataframe to store the new plotting
	prod_plan = pd.DataFrame()

	while min_intake_date_value > 0:
		min_intake_date = df_intake[df_intake['intake_balance']>0]['intake_date'].min()
		min_intake_date_value = df_intake[df_intake['intake_date']==min_intake_date]['intake_balance'].min()
		min_output_date = df_output[(df_output['output_balance'] > 0) & (df_output['output_date'] >= min_intake_date)]['output_date'].min()
		min_output_date_value = df_output[df_output['output_date']==min_output_date]['output_balance'].min()
		if np.isnan(min_intake_date_value):
			print('\nModel Message: All of the intake was plotted!!\n')
			break
		elif np.isnan(min_output_date_value):
			print('\nModel Message: Planned output numbers are less than planned intake, please plan for more output and try again!!\n')
			break
		new_output_value = min(min_intake_date_value, min_output_date_value)
		df_intake.loc[df_intake['intake_date']==min_intake_date, 'intake_balance'] = min_intake_date_value - new_output_value
		df_output.loc[df_output['output_date']==min_output_date, 'output_balance'] = min_output_date_value - new_output_value
		prod_plan = prod_plan.append({'intake_date': min_intake_date, 'output_date': min_output_date, 'stone_count': new_output_value}, ignore_index=True)

	df_intake['intake_plotted'] = df_intake['intake_count'] - df_intake['intake_balance']
	df_output['output_plotted'] = df_output['output_count'] - df_output['output_balance']
	prod_plan['bus_day_so_to_sc'] = np.busday_count(pd.to_datetime(prod_plan['intake_date']).values.astype('datetime64[D]'), pd.to_datetime(prod_plan['output_date']).values.astype('datetime64[D]'))
	tat_target = 2
	prod_plan['tat_target'] = tat_target
	prod_plan.loc[prod_plan['bus_day_so_to_sc'] <= prod_plan['tat_target'], 'tat_met'] = prod_plan['stone_count']
	prod_plan.loc[prod_plan['bus_day_so_to_sc'] > prod_plan['tat_target'], 'tat_met'] = 0






	print('Intake Details:.......\n', df_intake.sort_values(by='intake_date'), '\n')
	print('Output Details:.......\n', df_output.sort_values(by='output_date'), '\n')
	print('Production Plan:.......\n', prod_plan, '\n')
