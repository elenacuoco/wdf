__author__ = "Elena Cuoco"
__copyright__ = "Copyright 2017, Elena Cuoco"
__credits__ = []
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Elena Cuoco"
__email__ = "elena.cuoco@ego-gw.it"
__status__ = "Development"

 
from wdf.observers.observer import Observer
from wdf.observers.observable import Observable
 

 


class SegmentsObserver(Observer, Observable):
    def __init__(self):
        """
        :type self.parameters: class self.parameters object
        """
        Observable.__init__(self)
        Observer.__init__(self)
        self.segments_list = []

    def update(self, segment):
        self.segments_list.append(segment)
        self.update_observers(self.segments_list)
