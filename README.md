# Post-Experiment-Data-Analysis
This script is intended for the Titania Coatings group to ingest raw voltage data from the DAQ unit and create a plot with concentrations in ppb. The libraries/packages in the dependencies section should be installed.

## Dependencies
* [matplotlib](https://matplotlib.org/)
* [pandas](http://pandas.pydata.org/)

## Customization
The following can be tweaked by the user for further customization:
* `<self.margin>` in `<Experiment.init>`
* `<self.rolling_avg_window>` in `<Experiment.init>`
* all of the plotting parameters in `<Plot.init>`
