#import init_import
from common.checkscript import checkScipt
import logging,time,os

log = logging.getLogger(__name__)

def getVlnInfo(logfile):
    try:
        import tailer
        data = {}
    except:
        log.error("Can't load the tailer module.")
        
    if os.path.isfile(logfile):
        line = tailer.tail(open(logfile),1)
        status = line[0].split('[')[1].split(']')[0].split(':')[0]
        num = line[0].split('[')[1].split(']')[0].split(':')[1]
        data['status'] = status
        data['num'] = num
    else:
        log.error("Vln log file is not exits.%s" %logfile)

    return data
    
class Vln(checkScipt):
    def collector(self):
        print self.config
        data  = getVlnInfo(self.config['comman']['logFile'])
        self.add_guage('vln.num',data['num'])
        
# if __name__ == "__main__":
    # from common.utils.config import init_logging
    # init_logging()
    # import init_import
    # ps = Vln()
    # ps.debug()
    # print ps.getdataForm()
    