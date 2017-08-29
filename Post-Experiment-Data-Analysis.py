# # Titania Coatings - Post-Experiment Data Analysis
# This program is to take in data collected by the DAQ unit and output
# the results of that data, including plots and reductions
#
# Jesse Mendoza
# edited August 2017

import csv
import datetime as dt
import matplotlib.pyplot as plt
import pylab
import pandas as pd

class Experiment:
	def __init__(self):
		self.header_size=8

		#number of minutes to add before and after exp times
		self.margin = 1

		#number of samples (seconds) around each datapoint to use for rolling avg
		self.rolling_avg_window = 30

		self.duration = []
		self.no_ppb_raw = []
		self.nox_ppb_raw = []

	def conv_no_v_to_ppb(self, no_voltage):
		return 99.437*float(no_voltage) - 7.5526

	def conv_nox_v_to_ppb(self, nox_voltage):
		return 99.626*float(nox_voltage) + 0.66

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
		# start_margin added to take into consideration data points that
		# are removed from the beginning by the rolling average implementation
		start_margin = margin + dt.timedelta(seconds=self.rolling_avg_window)

		self.start_time = formatted_start_time - margin
		self.end_time = formatted_end_time + margin

		if (formatted_dt>(formatted_start_time-start_margin)) and (formatted_dt<(formatted_end_time+margin)):
			return True
		else:
			return False

	def get_duration(self, formatted_dt):
		diff = formatted_dt - self.start_time
		return round(float(diff.seconds)/60,2)

	def smooth_ppb(self):
		self.no_ppb_smooth = pd.Series(self.no_ppb_raw).rolling(window=self.rolling_avg_window,win_type='boxcar').mean()
		self.nox_ppb_smooth = pd.Series(self.nox_ppb_raw).rolling(window=self.rolling_avg_window,win_type='boxcar').mean()

	def reductions(self):
		self.no_ppb_min = self.no_ppb_smooth.min()
		self.nox_ppb_min = self.nox_ppb_smooth.min()
		self.no_ppb_max = self.no_ppb_smooth.max()
		self.nox_ppb_max = self.nox_ppb_smooth.max()
		self.no_reduction = 1-(self.no_ppb_min/self.no_ppb_max)
		self.nox_reduction = 1-(self.nox_ppb_min/self.nox_ppb_max)

	def run(self, datafile, exp_times):
		self.raw_data = self.get_dataset(datafile)
		listed_dataset = self.remove_headers(self.raw_data)
		self.date = listed_dataset[0][1].split(' ')[0]

		for row in listed_dataset:
			row[1] = self.transform_to_datetime(row[1])
			if self.filter_dataset(row[1], exp_times) == True:
				self.duration.append(self.get_duration(row[1]))
				self.no_ppb_raw.append(self.conv_no_v_to_ppb(row[2]))
				self.nox_ppb_raw.append(self.conv_nox_v_to_ppb(row[3]))
		self.smooth_ppb()
		self.reductions()
		return self


class Plot:
	def __init__(self, exp):
		pretty_start_time = exp.start_time.strftime("%I:%M %p")
		start_dt = exp.date + ', ' + pretty_start_time
		plt.title('NOx Reduction Experiment\n'+ start_dt)

		no=plt.plot(exp.duration, exp.no_ppb_smooth,label='NO')
		nox=plt.plot(exp.duration, exp.nox_ppb_smooth, label='NOx', color='r', linestyle='--')

		plt.xlabel('Duration (min)',size=12)
		plt.ylabel('Concentration (ppb)',fontsize=12)

		plt.legend(loc='best')

		plt.figtext(0.76,0.72,'Reductions', weight='bold')
		plt.figtext(0.76,0.68,'NO: {}%'.format(round(exp.no_reduction*100,1)))
		plt.figtext(0.76,0.64,'NOx: {}%'.format(round(exp.nox_reduction*100,1)))

		save_filename = "{}_{}".format(str(exp.date).replace('/','-'), pretty_start_time)
		pylab.savefig(save_filename)

		plt.show()


def main():
	print "\nWelcome to the Post-Experiment-Data-Analysis! Press Ctrl+C to exit anytime.\n"
	#datafile = raw_input("Raw DAQ data filename (in csv format): ")
	datafile = '1-19-17 CE-CERT.csv'
	'''exp_times_list = []
	exp_time = ''
	count = 1
	while exp_time != 'done':
		exp_time = raw_input("Reduction times of exp {}? Use format 1:30PM-1:50PM or 'done': ".format(count))
		exp_times_list.append(exp_time)
		count += 1'''
	exp_times_list = ['2:16PM-2:20PM']#,'3:09PM-3:22PM','3:51PM-3:58PM']

	for exp_times in exp_times_list:
		exp = Experiment().run(datafile,exp_times)
		Plot(exp)


if __name__ == '__main__':
	main()
