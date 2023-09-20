Introduction
=============

Wavelet detection filter (WDF) is a python library which wraps some of the routines in C++ of p4TSA and its python wrapper pytsa.
In WDF library you can find the WDF itself, that is a pipeline able to detect transient signal, using a wavelet decomposition 
of the data, followed by a denoising procedure, and later on by the estimation of the energy content of the signal.
In the same library you can find the whitening, and double whitneing (equivalent to dividing by the PSD the data) based on the AutoRegressive fit, 
which is implemented in time domain.
You can find also other functionalities linked to parametrice modeling (ARMA, AR, MA) or downsampling filter. 

Requirements
-------------

- p4TSA
- pytsa
- numpy
- scipy (upgraded version)
- docker with p4TSA and WDF environment

Installation
-------------

To install the wdf library, one has to run `setup.py` script from the main directory of the library.

``python setup.py install``

Howto
--------------
For a quick start, you can have a look at the Tutorial section

Contacts
---------------

If you find any issues, please contact:

- Elena Cuoco: elena.cuoco@ego-gw.it
- Filip Morawski: fmorawski@camk.edu.pl
- Alberto Iess: alberto.iess@sns.it
