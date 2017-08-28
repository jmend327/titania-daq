
# coding: utf-8

# # Titania Coatings - Post-Experiment Data Analysis
# This program is to take in data collected by the DAQ unit and output the results of that data, including plots and reductions
# 
# Jesse Mendoza
# edited August 2017

# ## Preface
# When calling script from bash, include filename and the times that the UV light was 
# turned on and when reduction stopped, in the following format. Please follow it exactly, punctuation and spaces and all: 
# 
# \>> python PostExperimentDataAnalysis.py 'experimentdata.csv' '2:30PM-2:55PM' '3:15PM-3:43PM'

'''
TODO:
Rolling average
Get date
Get reductions
Possibly cut more off end?
'''


import csv
import datetime as dt
import matplotlib.pyplot as plt
import os
import pylab
import matplotlib.text as t

'''import sys
import csv
import matplotlib.pyplot as plt
#get_ipython().magic('matplotlib inline')
import datetime as dt
import seaborn as sns
import os
import plotly
import pylab
import matplotlib.text as t'''



class Experiment:
	def __init__(self):
		self.header_size=8
		# margin = number of minutes to add before and after exp times
		self.margin = 1
		self.exp = {}
		self.exp['duration'] = []
		self.exp['no_ppb'] = []
		self.exp['nox_ppb'] = []


	def get_dataset(self, file_name):
		dataset = list(csv.reader(open(file_name,'r')))
		return dataset

	def remove_headers(self, dataset):
		return dataset[self.header_size:]

	def transform_to_datetime(self, datetime_string):
		split_dt_row = datetime_string.split(' ')
		split_dt_time = split_dt_row[1].split('.')
		formatted_time = dt.datetime.strptime(split_dt_time[0]+' '+split_dt_row[2],'%I:%M:%S %p')
		return formatted_time

	def filter_dataset(self, formatted_dt, exp_times):
		start_time = exp_times.split("-")[0]
		end_time = exp_times.split("-")[1]

		formatted_start_time = dt.datetime.strptime(start_time,'%I:%M%p')
		formatted_end_time = dt.datetime.strptime(end_time,'%I:%M%p')

		margin = dt.timedelta(minutes=self.margin)

		self.exp['start_time'] = formatted_start_time - margin
		self.exp['end_time'] = formatted_end_time + margin

		if (formatted_dt > (formatted_start_time-margin)) and (formatted_dt < (formatted_end_time+margin)):
			return True
		else:
			return False

	def get_duration(self, formatted_dt):
		diff = formatted_dt - self.exp['start_time']
		return round(float(diff.seconds)/60,2)

	def conv_no_v_to_ppb(self, no_voltage):
		return 99.437*float(no_voltage) - 7.5526

	def conv_nox_v_to_ppb(self, nox_voltage):
		return 99.626*float(nox_voltage) + 0.66

	def smooth_no_ppb(self,somethin):
		win = 60 #moving window (in seconds) 
		self.exp['no_ppb_smooth'] = self.exp['no_ppb'].rolling(window=win,win_type='boxcar').mean()
		self.exp['nox_ppb_smooth'] = self.exp['nox_ppb'].rolling(window=win,win_type='boxcar').mean()
	
	def kinetics(self):
		'''self.exp['no_ppb_min'] = self.exp['no_ppb_smooth'].min()
		self.exp['nox_ppb_min'] = self.exp['nox_ppb_smooth'].min()
		self.exp['no_ppb_max'] = self.exp['no_ppb_smooth'].max()
		self.exp['nox_ppb_max'] = self.exp['nox_ppb_smooth'].max()
		self.exp['no_reduction'] = 1-(self.exp['no_ppb_min']/self.exp['no_ppb_max'])
		self.exp['nox_reduction'] = 1-(self.exp['nox_ppb_min']/self.exp['nox_ppb_max'])'''
		pass

	def run(self, datafile, exp_times):
		self.exp['raw_data'] = self.get_dataset(datafile)
		listed_dataset = self.remove_headers(self.exp['raw_data'])

		for row in listed_dataset:
			row[1] = self.transform_to_datetime(row[1])
			if self.filter_dataset(row[1], exp_times) == True:
				self.exp['duration'].append(self.get_duration(row[1]))
				self.exp['no_ppb'].append(self.conv_no_v_to_ppb(row[2]))
				self.exp['nox_ppb'].append(self.conv_nox_v_to_ppb(row[3]))
		
		self.kinetics()

		'''for i,row in enumerate(self.exp['duration']):
			print row,'\t', self.exp['no_ppb'][i], '\t',self.exp['nox_ppb'][i]'''
		return self.exp



class Plot:
	def __init__(self, exp):
		self.plot_file_path = ''
	
		'''start_dt = str(exp.dataset['Date&Time'].iloc[0][0:16])+''+str(exp.dataset['Date&Time'].iloc[0][23:])
		plt.title('NOx Reduction\n'+'Experiment Starting @ '+ start_dt)'''
		
		no=plt.plot(exp['duration'], exp['no_ppb'],label='NO')
		nox=plt.plot(exp['duration'], exp['nox_ppb'], label='NOx', color='r', linestyle='--')
		
		plt.xlabel('Duration (min)',size=12)
		plt.ylabel('Concentration (ppb)',fontsize=12)
		
		plt.legend(loc='best')

		'''plt.figtext(0.765,0.72,'Reductions', weight='bold')
		plt.figtext(0.765,0.68,'NO: '+str(round(exp.no_reduction*100,1))+'%')
		plt.figtext(0.765,0.64,'NOx: '+str(round(exp.nox_reduction*100,1))+'%')'''
		
		#save_filename = str(start_dt[0:10]+'_'+exp.name).replace('/','-')
		save_filename = "Titania DAQ test"
		pylab.savefig('/Users/Owner/Desktop/'+save_filename)
		
		plt.show()


def main():
	print "\nHello, welcome to the Post-Experiment-Data-Analysis! Press Ctrl+C to exit anytime.\n"
	#datafile = raw_input("Raw DAQ data filename (in csv format): ")
	datafile = '1-19-17 CE-CERT.csv'
	'''exp_times_list = []
	exp_time = ''
	count = 1
	while exp_time != 'done':
		exp_time = raw_input("Reduction times of exp {}? Use format 1:30PM-1:50PM or 'done': ".format(count))
		exp_times_list.append(exp_time)
		count += 1'''
	exp_times_list = ['2:14PM-2:32PM','3:09PM-3:22PM','3:51PM-3:58PM']

	for exp_times in exp_times_list:
		exp = Experiment().run(datafile,exp_times)
		Plot(exp)


if __name__ == '__main__':
	main()




