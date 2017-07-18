# class Memory(object):
    # pass
from common.checkscript import checkScipt
import logging

log = logging.getLogger(__name__)

def get_meminfo():
    '''
    #Get the memory info freom /proc/meminfo
    '''
    try:
        data={}
        meminfo = open('/proc/meminfo')
        lines = meminfo.readlines()
        for line in lines:
            data[line.split()[0].split(':')[0]] = int(line.split()[1])
        data['MemUse']=data['MemTotal']-data['MemFree']
        return data
    except:
        log.error("Can't get meminfo from /proc/meminfo")
        return None
        
class Memory(checkScipt):
    def collector(self):
        ##Get config items for memory
        items = self.config['instance'][0]['items']
        
        ##Get the memory info freom /proc/meminfo
        meminfo = get_meminfo()
        if meminfo is not None and isinstance(meminfo,dict):
            for item in items:
                if meminfo.has_key(item):
                    self.add_guage('memory.'+item,meminfo[item])
        else:
            log.error("Get memory info data format is error")
        
# if __name__ == "__main__":
    # import init_import
    # from common.checkscript import checkScipt
    # from common.utils.config import init_logging

    # memory = Memory()
    # memory.debug()
    # print memory.getdataForm()
    