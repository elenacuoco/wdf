FROM wdfteam/env_wdf:2.2.2

#install wdpipe
RUN mkdir tmp1/
ADD . tmp1/
RUN cd tmp1/ && python setup.py  install &&\
    cd .. && rm -fr tmp1/ 

CMD ["/bin/bash"]
