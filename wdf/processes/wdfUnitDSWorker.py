__author__ = "Elena Cuoco"
__copyright__ = "Copyright 2017, Elena Cuoco"
__credits__ = []
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Elena Cuoco"
__email__ = "elena.cuoco@ego-gw.it"
__status__ = "Development"
import time

from pytsa.tsa import *
from pytsa.tsa import WaveletThreshold
from pytsa.tsa import SeqView_double_t as SV


from wdf.observers.ParameterEstimationObserver import ParameterEstimation 
from wdf.observers.SingleEventPrintFileObserver import SingleEventPrintTriggers
from wdf.processes.BandPassDownSampling import BandPassDownSampling
from wdf.config.Parameters import Parameters 
from wdf.processes.wdf import wdf
from wdf.processes.Whitening import Whitening 
from wdf.processes.DWhitening import DWhitening
import logging
import os

class wdfUnitDSWorker(object):
    def __init__(self, parameters, fullPrint=1):
        self.par = Parameters()
        self.par.copy(parameters)
        self.par.Ncoeff = parameters.window
        self.fullPrint = fullPrint
        self.par.channel = parameters.channel
        self.learn = parameters.learn
        self.par.resampling=parameters.sampling/parameters.ResamplingFactor
        self.par.len=parameters.len
           
    def segmentProcess(self, segment, wavThresh=WaveletThreshold.dohonojohnston):
        gpsStart, gpsEnd = segment[0],segment[1]
        logging.info(
            "Analyzing segment: %s-%s for channel %s downsampled at %dHz"
            % (gpsStart, gpsEnd, self.par.channel, self.par.resampling)
        )
        start_time = time.time()
        ID = "".join([str(self.par.channel),"_",str(int(gpsStart))])
        dir_chunk = "".join([self.par.outdir,self.par.run, "/", self.par.itf,"/",ID,'/'])
        # create the output dir
        if not os.path.exists(dir_chunk):
            os.makedirs(dir_chunk)
        if not os.path.isfile(dir_chunk + "ProcessEnded.check"):
            # self.parameter for whitening and its estimation self.parameters
            whiten = Whitening(self.par.ARorder)
            self.par.ARfile = dir_chunk + "ARcoeff-AR%s-fs%s-%s.txt" % (
                self.par.ARorder,
                self.par.resampling,
                self.par.channel,
            )
            self.par.LVfile = dir_chunk + "LVcoeff-AR%s-fs%s-%s.txt" % (
                self.par.ARorder,
                self.par.resampling,
                self.par.channel,
            )

            if os.path.isfile(self.par.ARfile) and os.path.isfile(self.par.LVfile):
                logging.info("Load AR parameters")
                whiten.ParametersLoad(self.par.ARfile, self.par.LVfile)
                 
            else:
                logging.info("Start AR parameter estimation")
                ######## read data for AR estimation###############
                # self.parameter for sequence of data.
                # Add a 100.0 seconds delay to not include too much after lock noise in
                # the estimation, not needed if working in DataScience segments
                #
                if gpsEnd - gpsStart >= self.learn + 100.0:
                    gpsE = gpsStart + 100.0
                else:
                    gpsE = gpsEnd - self.learn
                
                strLearn = FrameIChannel(
                    self.par.file, self.par.channel, self.learn, gpsE) 
                Learn = SV()
                Learn_DS = SV()
                ds = BandPassDownSampling(self.par,estimation=True)
                strLearn.GetData(Learn)
                Learn_DS=ds.Process(Learn)
                whiten.ParametersEstimate(Learn_DS)
                whiten.ParametersSave(self.par.ARfile, self.par.LVfile)
                
                del Learn, ds, strLearn, Learn_DS
                
            # sigma for the noise
            self.par.sigma = whiten.GetSigma()
            logging.info("Estimated sigma= %s" % self.par.sigma)
            
            # update the self.parameters to be saved in local json file
            self.par.ID = ID
            self.par.dir = dir_chunk
            self.par.gps = gpsStart
            self.par.gpsStart = gpsStart
            self.par.gpsEnd = gpsEnd-self.par.len

            ######################
            # self.parameter for sequence of data and the resampling
        
            ds = BandPassDownSampling(self.par)        
            
            #Perform operation to intialite the detection loop    
            #gpsStart = gpsStart - self.par.preWhite            
            data = SV()
            data_ds = SV()
            dataw = SV()
            Noutdata = int(self.par.resampling)
            DW=DWhitening(whiten.LV, Noutdata,0)
            for i in range(100):
                try:
                    streaming = FrameIChannel(self.par.file, self.par.channel, 1.0, gpsStart)
                    streaming.GetData(data)
                    break  # If no exceptions are thrown, exit the while loop
                except:
                    gpsStart=gpsStart+1.0
                    print("No frame, moving to the next one. New gpsStart is", gpsStart)
                continue  # If an exception is thrown, continue with the next iteration of the while loop
            ###---preheating---###
            streaming = FrameIChannel(self.par.file, self.par.channel, 1.0, gpsStart)
            # reading data, downsampling and whitening
            for i in range(self.par.preWhite):
                streaming.GetData(data)
                data_ds=ds.Process(data) 
                DW.Process(data_ds,dataw)
               
                
            #Set new size for the function in the loop
            streaming.SetDataLength(self.par.len)
           
            self.par.NoutData= int(self.par.resampling*self.par.len)
            DW.SetOutputSize(self.par.NoutData,0)    
            
            
            # WDF process
            WDF = wdf(self.par, wavThresh)
            
            # register obesevers to WDF process
            # put 0 to save only metaself.parameters, 1 for wavelet coefficients and 2
            # for waveform estimation, 3 for full event print
            savetrigger = SingleEventPrintTriggers(self.par, self.fullPrint)
            parameterestimation = ParameterEstimation(self.par)
            parameterestimation.register(savetrigger)
            WDF.register(parameterestimation)
            filejson = "parametersUsed.json"
            self.par.dump(self.par.dir + filejson)
            # Start detection loop
            logging.info("Starting detection loop")
            data = SV()
            data_ds = SV()
            dataw = SV()
            while data.GetStart() <=self.par.gpsEnd:
                streaming.GetData(data)
                data_ds=ds.Process(data)
                DW.Process(data_ds, dataw)
                WDF.SetData(dataw)
                WDF.Process()

            elapsed_time = time.time() - start_time
            timeslice = gpsEnd - gpsStart
            logging.info(
                "analyzed %s seconds in %s seconds" % (timeslice, elapsed_time)
            )
            fileEnd = self.par.dir + "ProcessEnded.check"
            open(fileEnd, "a").close()
        else:
            logging.info("Segment already processed")
