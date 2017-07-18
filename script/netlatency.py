# import init_import
from common.checkscript import checkScipt
import logging,time
import subprocess,re

log = logging.getLogger(__name__)


def getpingdata(dest):
    try:
        ping = subprocess.Popen(["ping", "-n", "-c 3", dest], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, error = ping.communicate()
        data={}
        if out:
            
            m=re.findall(r"\d+\.\d+",out)
            a=re.findall(r"\d+\%",out)
            data['MIN']=m[-4]
            data['AVG']=m[-3]
            data['MAX']=m[-2]
            data['LOSS']=a[0].split('%')[0]
        else:
            log.debug("Can't get ping info for %s" %dest)
        return data
    except:
        log.debug("Can't get ping info for %s" %dest)
             
class Netlatency(checkScipt):

    def collector(self):
        for instance in self.config['instance']:
            dest = instance['ip']
            data = getpingdata(dest)
            for item in instance['items']:
                if data.has_key(item.upper()):
                    key = 'latency.'+dest.replace('.','_')+'.'+item
                    self.add_guage(key,data[item.upper()])
                    
            
# if __name__ == "__main__":
    # from common.utils.config import init_logging
    # init_logging()
    # net = Netlatency()
    # net.debug()
    # print net.getdataForm()