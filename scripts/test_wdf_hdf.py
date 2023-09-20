import h5py
import os
from multiprocessing import Pool
from pytsa.tsa import *
from pytsa.tsa import SeqView_double_t as SV

from wdf.config.Parameters import *
from wdf.observers.ParameterEstimationObserver import *
from wdf.observers.SingleEventPrintFileObserver import *
from wdf.processes.Whitening import *
from wdf.processes.DWhitening import *
from wdf.structures.array2SeqView import *
from wdf.processes.wdf import wdf

def worker():
    logging.info("read Parameters")
    par = Parameters()
    par.load("config_hdf.json")
    par.outdir = os.getcwd() + "/out_data_"

    infile = par.dir + "/test.h5"

    
    f = h5py.File(infile, "r")

    f.keys()
    f.attrs.keys()
    par.gps = 0.0
    print(par.gps)
    ID = str(par.run) + "_" + str(par.channel) + "_" + str(int(par.gps))
    par.dir = par.outdir + ID + "/"
    
    outfile =  par.dir+ "outdata_white.h5"
    
    if not os.path.exists(par.dir):
        os.makedirs(par.dir)
    par.ID = ID
    # parameter for whitening and its estimation parameters
    whiten = Whitening(par.ARorder)
    par.ARfile = par.dir + "ARcoeff-AR%s-fs%s-%s.txt" % (
        par.ARorder,
        par.sampling,
        par.channel,
    )
    par.LVfile = par.dir + "LVcoeff-AR%s-fs%s-%s.txt" % (
        par.ARorder,
        par.sampling,
        par.channel,
    )
    ft = h5py.File(infile)
    chname = par.channel
    max_sec = f[chname].shape[0] / par.sampling
    max_sec = max_sec - 1

    whiten_proc = True
    # tm = TM()
    if os.path.isfile(par.ARfile) and os.path.isfile(par.LVfile):
        logging.info("Load AR parameter")
        whiten.ParametersLoad(par.ARfile, par.LVfile)
        # whiten_proc=False
    else:
        logging.info("Start AR parameter estimation")
        ######## read data for AR estimation###############
        # Parameter for sequence of data

        N = int(par.learn * par.sampling)
        harr = ft[chname]
        t1i = 0
        t2i = N
        arrayLearn = harr[t1i : t2i + 1]
        Learn = array2SeqView(par.gps, par.sampling, N)
        Learn = Learn.Fill(par.gps, arrayLearn)
        whiten.ParametersEstimate(Learn)
        whiten.ParametersSave(par.ARfile, par.LVfile)
        del Learn
    ######################
    # Parameter for sequence of data
    # read data

    ### WDF process
    # sigma for the noise
    par.sigma = 2.0 * whiten.GetSigma()
    print("Estimated sigma= %s" % par.sigma)
    par.Ncoeff = par.window
    WDF = wdf(par, WaveletThreshold.dohonojohnston)
    # WDF = wdf(par)
    par.resampling = par.sampling
    savetrigger = SingleEventPrintTriggers(par, fullPrint=2)
    parameterestimation = ParameterEstimation(par)
    parameterestimation.register(savetrigger)
    WDF.register(parameterestimation)
    ###Start detection loop
    print("Starting detection loop")
    tmin = par.gps
    dataw = SV()
    harr = ft[chname]
    # num elements per each loop
    nel = int(par.len * par.sampling)
    t1i = 0
    t2i = nel
    DW=DWhitening(whiten.LV, nel,0)
       
    if whiten_proc:
        tsel_proc = np.empty(nel)
        # save out
        outf = h5py.File(outfile, "a")
        new_dataset = outf.create_dataset(
            chname + "_white", (max_sec * (nel),), chunks=(nel,), compression="gzip"
        )
    t = 0
    while t2i <= max_sec * nel:  # len(harr):
        tsel = harr[t1i:t2i]
        # do whitening or else here,e.g. just multiply by 3
        data = array2SeqView(tmin, par.sampling, nel)
        data = data.Fill(tmin, tsel)
        DW.Process(data, dataw)
        if whiten_proc:
            for i in range(nel):
                tsel_proc[i] = dataw.GetY(0, i)
            new_dataset[t1i:t2i] = tsel_proc
            for ai in ft[chname].attrs.keys():
                new_dataset.attrs[ai] = ft[chname].attrs[ai]

            for ai in ft.attrs.keys():
                outf.attrs[ai] = ft.attrs[ai]
            outf.flush()
        WDF.SetData(dataw)
        WDF.Process()
        t1i = t2i
        t2i = t1i + nel
        tmin += par.len
        print(t)
        t += 1
    if whiten_proc:
        outf.close()
        outf = h5py.File(outfile, "r")
        print(list(outf.keys()))
        outf.close()

    par.dump(par.dir + "fileParametersUsed.json")
    # elapsed_time = time.time() - start_time
    # timeslice =tmin- par.gps
    # print('analyzed %s seconds in %s seconds' % (timeslice, elapsed_time))


if __name__ == "__main__":  # pragma: no cover
    worker()
