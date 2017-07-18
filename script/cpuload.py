# import init_import
from common.checkscript import checkScipt
import logging,time

log = logging.getLogger(__name__)

import os 
def load_stat(): 
    loadavg = {} 
    f = open("/proc/loadavg") 
    con = f.read().split() 
    f.close() 
    loadavg['LOAD1']=con[0] 
    loadavg['LOAD5']=con[1] 
    loadavg['LOAD15']=con[2] 
    loadavg['NR']=con[3] 
    loadavg['LASTPID']=con[4] 
    return loadavg 

class Cpuload(checkScipt):
    def collector(self):
        cpuload = load_stat() 
        for item in self.config['instance'][0]['items']:
            if cpuload.has_key(item):
                key = 'load.'+item
                value = cpuload[item]
                self.add_guage(key,value)
        
 
# if __name__ == "__main__":
    # import init_import
    # cpu = Cpuload()
    # cpu.debug()
    # print cpu.getdataForm()
       
