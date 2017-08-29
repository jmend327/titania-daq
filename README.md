# Post-Experiment-Data-Analysis
This script is intended for the Titania Coatings roup to ingest raw voltage data from the DAQ unit and create a plot with concenrations in ppb. The libraries/packages in the dependencies section should be installed, then the following tweaks should be made for customization:
    self.margin in Experiment.__init__
    self.rolling_avg_window in Experiment.__init__
    all of the plotting parameters in Plot.__init__

## Dependencies
matplotlib
pylab
pandas
