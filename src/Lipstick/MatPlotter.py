'''
Created on Mar 14, 2012

@author: elifinkelshteyn
'''

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
class MatPlotter(object):
    '''
    Takes in data from a run of pig and uses it to create some pretty graphs
    using matplotlib
    '''

    def __init__(self, coords):
        (x, y) = (coords[0], coords[1])
        x = [datetime.strptime(day, "%Y/%m/%d") for day in x]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot_date(x, y, '-')
        ax.xaxis.set_major_locator( mdates.DayLocator() )
        #ax.xaxis.set_minor_locator( mdates.HourLocator(numpy.arange(0,25,6)) )
        ax.xaxis.set_major_formatter( mdates.DateFormatter('%Y-%m-%d') )
        plt.show()
        
    def get_sample(self):
        days = ['2012/02/19', '2012/02/20', '2012/02/21', '2012/02/22']
        nums = [12341, 34523, 56435, 94634]  
        return (days, nums) 