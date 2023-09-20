__author__ = "Elena Cuoco"
__copyright__ = "Copyright 2017, Elena Cuoco"
__credits__ = []
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Elena Cuoco"
__email__ = "elena.cuoco@ego-gw.it"
__status__ = "Development"

import logging
import time

from pytsa.tsa import FrameIChannel
from pytsa.tsa import SeqView_double_t as SV
from wdf.observers.observable import Observable

logging.basicConfig(level=logging.DEBUG)


def defineStateVector(stateVector, flag):
    mask = pow(2, flag)
    state = stateVector & mask
    return state == mask


class createSegments(Observable):
    def __init__(self, parameters):
        """
        :type parameters: class Parameters
        """
        Observable.__init__(self)
        self.file = parameters.file
        self.state_chan = parameters.status_itf
        self.gps = parameters.gps
        self.minSlice = parameters.minSlice
        self.lastGPS = parameters.lastGPS
        self.flag = int(parameters.flag)

    def Process(self):
        itfStatus = FrameIChannel(self.file, self.state_chan, 1.0, self.gps)
        Info = SV()
        timeslice = 0.0
        start = self.gps
        last = False
        fails = 0
        iter_fails = 0
        first_fail_gps=0
        while start <= self.lastGPS:
            try:
                itfStatus.GetData(Info)
            except BaseException:
                if iter_fails == 0:  # online
                    logging.warning(
                        "GPS time: %s. Waiting for new acquired data" % start
                    )
                    time.sleep(100)
                    iter_fails += 1
                    timeslice += 1
                else:
                    timeslice = 0
                    fails += 1
                    start += 1.0
                    itfStatus = FrameIChannel(self.file, self.state_chan, 1.0, start)        
                continue
                first_fail_gps=start-fails     
                logging.error("DAQ PROBLEM from GPS %s to GPS %s" %(first_fail_gps,start))
            else:
                start = Info.GetX(0)
                iter_fails = 0
                stateVector = int(Info.GetY(0, 0))
                status = defineStateVector(stateVector, self.flag)
            
                if status:
                    timeslice += 1.0
                else:
                  if timeslice >= self.minSlice:
                        gpsEnd = start
                        gpsStart = gpsEnd - timeslice
                        logging.info(
                            "New segment created: Start %s End %s Duration %s"
                            % (gpsStart, gpsEnd, timeslice)
                        )
                        self.update_observers([[gpsStart, gpsEnd]], last)
                        logging.info("Total Fails: %s" % fails)
                  timeslice = 0.0
                if start == self.lastGPS:
                    logging.info("Segment creation completed")
                    self.unregister_all()
                    break


