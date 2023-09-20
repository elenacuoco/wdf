import logging
from wdf.observers.observer import Observer
from wdf.observers.observable import Observable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SingleEventTriggers(Observer, Observable):
    """
    This class stands for the conversion to dictionary generated single trigger
    """
    def __init__ ( self,  parameters, channel: str):
        """
        This class stands for the conversion to dictionary generated single trigger

        :type parameters
        :param parameters: Set of parameters

        :type channel: int
        :param channel: string with the name of the channel to analyse
        """

        Observable.__init__(self)
        Observer.__init__(self)

        self.parameters = parameters
        self.id = 0
        self.channel = channel
        self.fullPrint = parameters.fullPrint
        self.headers = ["gps","gpsPeak", "duration","EnWDF", "snrMean", "snrPeak", "freqMin","freqMean", "freqMax","freqPeak", "wave"]
    
        self.headersWavelets =  ["gps","gpsPeak", "duration","EnWDF", "snrMean", "snrPeak", "freqMin","freqMean", "freqMax","freqPeak", "wave"]         
        
        self.headersWaveform = ["gps","gpsPeak", "duration","EnWDF", "snrMean", "snrPeak", "freqMin","freqMean", "freqMax","freqPeak", "wave"] 
        
        self.headersFull = ["gps","gpsPeak", "duration","EnWDF", "snrMean", "snrPeak", "freqMin","freqMean", "freqMax","freqPeak", "wave"] 

        for i in range(parameters.Ncoeff):
            self.headers.append("wt" + str(i))
            self.headersWavelets.append("wt" + str(i))
            self.headersFull.append("wt" + str(i))
            
        for i in range(parameters.Ncoeff):
            self.headersFull.append("rw" + str(i))
            self.headersWaveform.append("rw" + str(i))


    def update(self, CEV: object):
        """
        :type CEV: object
        :param CEV: The object storing single trigger data
        :return: single trigger in the form of dictionary
        """
        self.ev = CEV.__dict__
        
        self.id += 1
        self.ev['ID'] = self.id
        trigger_content = None
        if self.fullPrint == 0:
            # Filter the dictionary to only include the headers 
            trigger_content = dict(
                    (k, self.ev[k])
                    for k in (
                          "gps","gpsPeak", "duration","EnWDF", "snrMean", "snrPeak", "freqMin","freqMean", "freqMax","freqPeak", "wave"
                    )
                )
        if self.fullPrint == 1:
            trigger_content = dict((k, self.ev[k]) for k in self.headersWavelets)
        if self.fullPrint == 2:
            trigger_content = dict((k, self.ev[k]) for k in self.headersWaveform)
        if self.fullPrint == 3:
            trigger_content = dict((k, self.ev[k]) for k in self.headersFull)

        self.update_observers(trigger_content, self.ev["Ncoeff"])
