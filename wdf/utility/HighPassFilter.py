import logging
from wdf.structures.array2SeqView import *
import numpy as np
from scipy.signal import butter, lfiltic,lfilter,filtfilt

def SV_to_array(seqView):
    x = np.zeros(seqView.GetSize())
    y = np.zeros(seqView.GetSize())
    for i in range(seqView.GetSize()):
        x[i] = seqView.GetX(i)
        y[i] = seqView.GetY(0,i)
    return x,y

class HighPassFilter(object):
    
    def __init__(self, cutoff_freq, sampling_rate, filter_order=6):
        self.cutoff_freq = cutoff_freq
        self.sampling_rate = sampling_rate
        self.filter_order = filter_order
      
        
        # Calculate the filter coefficients using Butterworth filter design
        nyquist_rate = 0.5 * self.sampling_rate
        normalized_cutoff_freq = self.cutoff_freq / nyquist_rate
        self.b, self.a = butter(self.filter_order, normalized_cutoff_freq, btype='high', analog=False)
        self.zi = lfiltic(self.b, self.a, [0])
        
      
    
    def Process(self, data):
        y = np.zeros(data.GetSize())
        x = np.zeros(data.GetSize())
        
        x, y = SV_to_array(data)
     
        filtered_signal, self.zi = lfilter(self.b, self.a, y, zi=self.zi)
         
         
        datahp = array2SeqView(data.GetStart(),self.sampling_rate, data.GetSize())
        datahp.Fill(data.GetStart(), array=filtered_signal)
        datahp=datahp.SV
        
        return datahp
    
     