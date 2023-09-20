__author__ = "Elena Cuoco"
__project__ = "wdf"
 
from pytsa.tsa import SeqView_double_t as SV
from pytsa.tsa import FrameIChannel
from wdf.observers.observable import Observable
from wdf.structures.segment import *
import logging
import time

logging.basicConfig(level=logging.INFO)


class createSegmentsMinMax(Observable):
    def __init__(self, parameters):
        """
        :type parameters: class Parameters
        """
        Observable.__init__(self)
        self.file = parameters.file
        self.state_chan = parameters.status_itf
        self.gps = parameters.gps
        self.minSlice = parameters.minSlice
        self.maxSlice = parameters.maxSlice
        self.lastGPS = parameters.lastGPS
        self.flag = parameters.flag

    def Process(self):
        itfStatus = FrameIChannel(self.file, self.state_chan, 1.0, self.gps)
        Info = SV()
        timeslice = 0.0
        start = self.gps
        last = False
        fails = 0
        iter_fails = 0
        while start <= self.lastGPS:
            try:
                itfStatus.GetData(Info)
            except BaseException:
                if iter_fails == 0:  # online
                    logging.warning(
                        "GPS time: %s. Waiting for new acquired data" % start
                    )
                    time.sleep(1000)
                    iter_fails += 1
                    timeslice += 1
                else:
                    timeslice = 0
                    logging.error("FLAG not passed @GPS %s" % start)
                    fails += 1
                    start += 1.0
                    itfStatus = FrameIChannel(self.file, self.state_chan, 1.0, start)
            else:
                start = Info.GetX(0)
                iter_fails = 0
                # if Info.GetY(0, 0) == 0:
                #    logging.error("MISSING DATA @GPS %s" % start)
                #    fails += 1
                if Info.GetY(0, 0) in self.flag:
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
                        logging.error("Total Fails: %s" % fails)
                    timeslice = 0.0

                if timeslice >= self.maxSlice:
                    gpsEnd = start
                    gpsStart = gpsEnd - timeslice
                    logging.info(
                        "New science segment created: Start %s End %s Duration %s"
                        % (gpsStart, gpsEnd, timeslice)
                    )
                    self.update_observers([[gpsStart, gpsEnd]], last)
                    timeslice = 0.0

                if start == self.lastGPS:
                    logging.info("Segment creation completed")
                    self.unregister_all()
                    break
