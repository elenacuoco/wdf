__author__ = "Elena Cuoco"
__project__ = "wdf"


import logging
from wdf.structures.array2SeqView import *
import numpy as np
from scipy.signal import butter, filtfilt,lfilter,lfilter_zi 


 
def SV_to_array(seqView):
    y = np.zeros(seqView.GetSize())
    for i in range(seqView.GetSize()):
        y[i] = seqView.GetY(0,i)
    return y

 



class DownSamplingLF(object):
    """
    The downsampling class base on scipy and numpy library
    """

    def __init__(self, Parameters,order=9):
        """
        The constructor

        :type Parameters: dict
        :param Parameters: The dictionary containing list of parameters
        """
        try:
            self.sampling = int(Parameters.sampling)
        except ValueError:
            logging.error("sampling not defined")
        try:
            self.resampling = int(Parameters.resampling)
        except ValueError:
            logging.error("Resampling  not defined")
        try:
            self.ResamplingFactor = int(Parameters.ResamplingFactor)
        except ValueError:
            logging.error("Resampling factor not defined")

        self.order=order
        # Apply a low-pass filter to the data to prevent aliasing
        self.nyquist_frequency = 0.5 * self.sampling
        self.cutoff_frequency =  0.95*(self.nyquist_frequency / self.ResamplingFactor)

        # Set the default filter order if not specified
        if order is None:
            self.order = 8

        self.b, self.a = butter(self.order,self.cutoff_frequency / self.nyquist_frequency, 'low') 
       # Get the steady state of the filter's step response.
        self.filter_forw =lfilter_zi(self.b,self.a) # Initialize the filter state 
         
        self.first_call=True
         
        
    def Process(self, data):
        """
        The method for the downsampling the data
        """
        
        #dimension of decimated data 
        Noutdata=int(data.GetSize()/self.ResamplingFactor)
        #filtered signal array
        y_f = np.zeros(data.GetSize())
        #decimate signal array
        y_ds = np.zeros(Noutdata)
        #signal array
        y = SV_to_array(data) 
       
        
        if self.first_call==True: 
            y_f=filtfilt(self.b,self.a,y)
            self.first_call=False
        else:    
            zi = self.filter_forw
            (y_f, zf) = lfilter(self.b, self.a, y, zi=zi)      
            self.filter_forw=zf
        
           
  
        # Downsample the filtered data
        
        y_ds= y_f[::self.ResamplingFactor]
        
         
        data_ds = array2SeqView(data.GetStart(),self.resampling, Noutdata)
        data_ds.Fill(data.GetStart(), array=y_ds)
        data_ds=data_ds.SV

        return data_ds


  