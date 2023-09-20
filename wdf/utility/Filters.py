__author__ = "Elena Cuoco"
__project__ = "wdf"

 
import numpy as np
from scipy.signal  import butter,filtfilt
from wdf.structures.array2SeqView import *

class Butterworth(object):

    """
    This class implement a series of filtering low, band and high pass, using scipy signal library for SeqView structures and for numpy array
    """

    def __init__(self, frequency, sampling, order, filtertype):
        """inititialite for low or high pass filter using Butterworth model. It is advisable an offline design study of the filter
        Arguments:
            frequency {double} -- low or high cut
            sampling {double} -- sampling frequency of the signal
            order {integer} -- order of Butterworth filter
            filtertype {string} -- option for low or high pass 
        """        
        self.sampling=sampling
        self.cutoff = frequency/(0.5*sampling)
        self.filtertype=str(filtertype)
        self.b, self.a = butter(order, self.cutoff, btype=self.filtertype, analog=False)


    def ProcessSeq(self, data):
        """Filter data with Butterworth filter

        Arguments:
            data {SeqView} -- pytsa SeqView

        Returns:
            SeqView -- filtered SeqView
        """
        
        y=np.zeros(data.GetSize())
        yf=np.zeros(data.GetSize())
         
        for i in range(data.GetSize()):
            y[i]=data.GetY(0,i)

        
        yf=filtfilt(self.b, self.a, y)
        
        dataf = array2SeqView(data.GetStart(), self.sampling, len(yf))
        dataf=dataf.Fill(data.GetStart(), yf)
        
        return   dataf

    def Process(self, data):
        """Implement the filter for numpy array

        Arguments:
            data {numpy array} -- input raw data
            dataf {numpy array} -- output filtered data

        
        """ 
        dataf=np.array(len(data))       
        dataf=filtfilt(self.b, self.a, data)  
        return   dataf