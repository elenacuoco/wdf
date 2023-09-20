__author__ = "Elena Cuoco"
__copyright__ = "Copyright 2017, Elena Cuoco"
__credits__ = []
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Elena Cuoco"
__email__ = "elena.cuoco@ego-gw.it"
__status__ = "Development"

import csv
import os.path
from wdf.observers.observer import Observer
 


class SingleEventPrintTriggers(Observer):
    """
    The class defining methods to save single event

    """

    def __init__(self, par, fullPrint=0):
        """
        The constructor

        :type par: dict
        :param observer: The dictionary of WDF parameters
        :type fullPrint: int
        :param fullPrint: Flag for the output type: 0 - metadata, 3 - wavelet coefficients, 2 - reconstructed wavelet

        """
        self.filesave = par.dir + "WDFTriggers-%s-GPS%s-AR%s-Win%s-Ov%s-EnWDF%s.csv" % (
            par.channel.replace(':', '-'),
            int(par.gps),
            par.ARorder,
            par.window,
            par.overlap,
            str(par.threshold),
        )
        self.id = 0
        if os.path.isfile(self.filesave):
            try:
                os.remove(self.filesave)
            except OSError:
                pass
        self.fullPrint = fullPrint
                    
        self.headers = ["gps","gpsPeak", "duration","EnWDF", "snrMean", "snrPeak", "freqMin","freqMean", "freqMax","freqPeak", "wave"]
    
        self.headersWavelets =  ["gps","gpsPeak", "duration","EnWDF", "snrMean", "snrPeak", "freqMin","freqMean", "freqMax","freqPeak", "wave"]         
        
        self.headersWaveform = ["gps","gpsPeak", "duration","EnWDF", "snrMean", "snrPeak", "freqMin","freqMean", "freqMax","freqPeak", "wave"] 
        
        self.headersFull = ["gps","gpsPeak", "duration","EnWDF", "snrMean", "snrPeak", "freqMin","freqMean", "freqMax","freqPeak", "wave"] 

        for i in range(par.Ncoeff):
            self.headers.append("wt" + str(i))
            self.headersWavelets.append("wt" + str(i))
            self.headersFull.append("wt" + str(i))
            
        for i in range(par.Ncoeff):
            self.headersFull.append("rw" + str(i))
            self.headersWaveform.append("rw" + str(i))

            # write on disk in ordered way

    def update(self, CEV):
        """
        This methods saves the triggers to the csv file

        :type eventPE: pytsa object
        :param eventPE: Metadata, wavelet coefficients and reconstructed wavelets of the trigger
        
        :param CEV: pytsa object that contains metadata, wavelet coefficients and reconstructed wavelets of the trigger.

        :type CEV: pytsa object
        """

        # Check if the file already exists
        self.file_exists = os.path.isfile(self.filesave)
        # Get the attributes of CEV as a dictionary
        self.ev = CEV.__dict__
        # Increment the ID counter
        self.id += 1
        self.ev["ID"] = self.id
        # Write to the csv file based on the fullPrint attribute
        if self.fullPrint == 0:
            with open(self.filesave, "a") as csvfile:
                  # Set the headers for the csv file
                headers =  ["gps","gpsPeak", "duration","EnWDF", "snrMean", "snrPeak", "freqMin","freqMean", "freqMax","freqPeak", "wave"]
                # Filter the dictionary to only include the headers 
                toprint = dict(
                    (k, self.ev[k])
                    for k in (
                          "gps","gpsPeak", "duration","EnWDF", "snrMean", "snrPeak", "freqMin","freqMean", "freqMax","freqPeak", "wave"
             
                    )
                )
                 # Create the csv writer object
                writer = csv.DictWriter(
                    csvfile, delimiter=",", lineterminator="\n", fieldnames=headers
                )
                  # If the file doesn't exist, write the headers
                if not self.file_exists:
                    writer.writeheader()
                 # Write the row to the csv file
                writer.writerow(toprint)
        # Write to the csv file based on the fullPrint attribute
        if self.fullPrint == 1:
            with open(self.filesave, "a") as csvfile:
                # Create the csv writer object 
                writer = csv.DictWriter(
                    csvfile, delimiter=",", lineterminator="\n", fieldnames=self.headersWavelets
                )
                toprint = dict((k, self.ev[k]) for k in self.headersWavelets)
                if not self.file_exists:
                    writer.writeheader()
                writer.writerow(toprint)
        if self.fullPrint == 2:
            with open(self.filesave, "a") as csvfile:
                 # Create the csv writer object 
                writer = csv.DictWriter(
                    csvfile,
                    delimiter=",",
                    lineterminator="\n",
                    fieldnames=self.headersWaveform,
                )
                toprint = dict((k, self.ev[k]) for k in self.headersWaveform)
                if not self.file_exists:
                    writer.writeheader()
                writer.writerow(toprint)
        if self.fullPrint == 3:
            with open(self.filesave, "a") as csvfile:
                # Create the csv writer object
                writer = csv.DictWriter(
                    csvfile,
                    delimiter=",",
                    lineterminator="\n",
                    fieldnames=self.headersFull,
                )
                toprint = dict((k, self.ev[k]) for k in self.headersFull)
                if not self.file_exists:
                    writer.writeheader()
                writer.writerow(toprint)
