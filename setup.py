from distutils.core import setup 
 
with open('version.txt', 'r') as fp:
    __version__ = fp.readline().strip()
    print("version %s" %__version__)
 
setup( 
    name="wdf",
    version=__version__,
    author="Elena Cuoco ",
    description="WDF pipeline library",
    author_email="elena.cuoco@ego-gw.it",
    url="https://wdfpipe.gitlab.io/",
    packages=['wdf','wdf.config', 'wdf.processes','wdf.observers','wdf.structures','wdf.utility'] 
     )