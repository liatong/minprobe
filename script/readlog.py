# import init_import
from common.checkscript import checkScipt
import logging,time,os

log = logging.getLogger(__name__)

def readloginfo(logfile):
    try:
        import tailer
        data = {}
    except:
        log.error("Can't load the tailer module.")
        
    if os.path.isfile(logfile):
        line = tailer.tail(open(logfile),1)
        status = line[0].split('[')[1].split(']')[0].split(':')[1]
        data['status'] = status
    else:
        log.error("Log file is not exits.%s" %logfile)

    return data
    
class Readlog(checkScipt):
    def collector(self):
        print self.config
        for ins in  self.config['instance']:
            data = readloginfo(ins['file'])
            self.add_guage(ins['items']['key'],data['status'])
        
# if __name__ == "__main__":
    # from common.utils.config import init_logging
    # init_logging()
    # import init_import
    # ps = Readlog()
    # ps.debug()
    # print ps.getdataForm()
    