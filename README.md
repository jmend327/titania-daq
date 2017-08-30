# Post-Experiment-Data-Analysis
This script is intended for the Titania Coatings group to ingest raw voltage data from the DAQ unit and create a plot with concentrations in ppb. The libraries/packages in the __Dependencies__ section must be installed before running this script.

## Dependencies
* [matplotlib](https://matplotlib.org/)
* [pandas](http://pandas.pydata.org/)

## Customization
The following can be tweaked by the user for further customization:
* `self.margin` in `Experiment.init`
* `self.rolling_avg_window` in `Experiment.init`
* all of the plotting parameters in `Plot.init`

You can run the `test.sh` shell script to try out this program. It should ingest the csv file in the `test` folder and use the input in `input.txt`, then display 2 plots.
