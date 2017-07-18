#import init_import
from common.checkscript import checkScipt
import logging,time

log = logging.getLogger(__name__)

def getProStat(list):
    try:
        import psutil
    except:
        log.error("Can't load module psutil")
    data={}
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid','name','cmdline','memory_percent','cpu_percent','num_threads'])
        except:
            pass
        else:
            if pinfo['name'] in list and len(pinfo['cmdline']) > 0 :
                data[pinfo['name']]=pinfo
    return data
    
class Process(checkScipt):

    def collector(self):
        #print self.config
        list = map(lambda x:x['process'],self.config['instance'])
        data = getProStat(list)
        for proc in list:
            if proc in data.keys():
                self.add_guage('process.'+proc+'.'+'status',1)
                self.add_guage('process.'+proc+'.'+'num_threads',data[proc]['num_threads'])
                self.add_guage('process.'+proc+'.'+'cpu_percent',data[proc]['cpu_percent'])
                self.add_guage('process.'+proc+'.'+'memory_percent',round(data[proc]['memory_percent'],2))
            else:
                self.add_guage('process.'+proc+'.status',0)
                #print "%s no running " %proc
                        
# if __name__ == "__main__":
    # from common.utils.config import init_logging
    # init_logging()
    # import init_import
    # ps = Process()
    # ps.debug()
    # print ps.getdataForm()
    