# import libraries
import time
import os
from pytsa.tsa import *
from pytsa.tsa import SeqView_double_t as SV
from wdf.config.Parameters import *
from wdf.processes.wdfUnitDSWorker import *
import logging
import coloredlogs
#select level of logging
coloredlogs.install(isatty=True)
import multiprocessing as mp
 
logging.basicConfig(level=logging.INFO)

def main(par):
   

    par.print() 
    start_time = time.time()
    par.dir=os.getcwd()+'/'+par.dir
    par.outdir=os.getcwd()+'/'+par.outdir
    strInfo = FrameIChannel(par.file, par.channel, 1.0, par.gps)
    Info = SV()
    strInfo.GetData(Info)
    par.sampling = int(1.0 / Info.GetSampling())    
    par.resampling = int(par.sampling / par.ResamplingFactor)
    logging.info("sampling frequency= %s, resampled frequency= %s" %(par.sampling, par.resampling))
    del Info, strInfo
    print("Number of processors: ", mp.cpu_count())
    pool = mp.Pool(par.nproc) 
    wdf=wdfUnitDSWorker(par,fullPrint=0)
    pool.map(wdf.segmentProcess, [segment for segment in par.segments])
    pool.close()     

    # 
    logging.info("Program terminated")
    par.dump(par.outdir + "fileParametersUsed.json")
    


if __name__ == "__main__":
    logging.info("read parameters from JSON file")
    param = Parameters()
    filejson = "input.json"         
    try:
        param.load(filejson)
    except IOError:
        logging.error("Cannot find resource file " + filejson)
        quit()   
    main(param)
