__author__ = "Elena Cuoco"
__project__ = "wdf"

from pytsa.tsa import WDF2Reconstruct, EventFullFeatured
from pytsa.tsa import WaveletThreshold
from wdf.observers.observable import Observable
 


class wdf_reconstruct(Observable):

    """
    The main WDF class responsible for the communication with the p4TSA library regarding the application of WDF onto data
    """

    def __init__(self, parameters, wTh=WaveletThreshold.dohonojohnston):
        """
        The main WDF class responsible for the communication with the p4TSA library regarding the application of WDF onto data

        :type parameters: WdfParam
        :param parameters: Set of WDF parameters

        :type wth: pytsa.WaveletThreshold
        :param wavThresh: Type of wavelet thresholding function; default value = WaveletThreshold.dohonojohnston

        """
        Observable.__init__(self)
        self.parameters = parameters
        self.wdf2reconstruct = WDF2Reconstruct(
            self.parameters.window,
            self.parameters.overlap,
            self.parameters.threshold,
            self.parameters.sigma,
            self.parameters.Ncoeff,
            wTh,
        )
        self.trigger = EventFullFeatured(self.parameters.Ncoeff)

    def SetData(self, data):
        """
        This methods sets sets the data for the p4TSA wdf2reconstruct class for further search of triggers

        :type data: pytsa.SeqViewDouble
        :param data: An pytsa.SeqViewDouble object storing data to be processed

        """
        # to be multiplied by central frequency
        self.wdf2reconstruct(data, self.parameters.sigma)

    def FindEvents(self):
        """
        This method calls wdf2reconstruct function from pytsa to search for triggers in the data

        :return: trigger
        """
        # to be multiplied by central frequency
        self.wdf2reconstruct(self.trigger)
        return self.trigger

    def Process(self):
        """
        This method calls wdf2reconstruct function from pytsa to search for triggers in the data
        If the triggers are found, they are stored in tosend_triggers variable that is later on used for further processing

        """
        while self.wdf2reconstruct.GetDataNeeded() > 0:
            m = self.wdf2reconstruct(self.trigger)
            if m == 1:
                self.update_observers(self.trigger)
