__author__ = "Elena Cuoco"
__project__ = "wdf"

from pytsa.tsa import ARMAFilter, ArBurgEstimator
 


class Coloring(object):

    """
    This class implement the inverse whitening functions from pytsa
    """

    def __init__(self, ARorder):
        """
        This class is responsible for the communiction with whitening functions from pytsa

        :type ARorder: int
        :param ARorder: The order for AutoRegressive filter
        """
        self.ARorder = ARorder
        self.ADE = ArBurgEstimator(self.ARorder)

    def ParametersLoad(self, ARfile):
        """
        This method loads the calculated AR and LV parameter from the file

        :type ARfile: basestring
        :param ARfile: file for AutoRegressive parameters


        :return: Autoregressive  View
        """

        self.ADE.Load(ARfile, "txt")
        arorder=self.ARorder+1
        self.ARMAflt=ARMAFilter(arorder,1,self.ADE.GetAR(0)) 
        self.ARMAflt.SetARFilter(0,1.0)
        
        for i in range(1, arorder):
            self.ARMAflt.SetARFilter(i,self.ADE.GetAR(i))
            
        self.ARMAflt.SetMAFilter(0,self.ADE.GetAR(0))
        
        
    def Process(self, dataw, datac):
        """
        This method color the data by calling proper function from pytsa

        :param dataw: pytsa.SeqViewDouble
        :param datac: pytsa.SeqViewDouble
        """

        self.ARMAflt(dataw, datac)
