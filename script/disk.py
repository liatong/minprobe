# import init_import
from common.checkscript import checkScipt
import subprocess
import logging,time

log = logging.getLogger(__name__)

def getDisk():
    COMMAND=['df','-T']
    ITEM=['DEV','TOTAL','USE','FREE','PRE','MOUNT']
    data={}
    try:
        proc = subprocess.Popen(COMMAND,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        (stdout,stdin)=proc.communicate()
        lines = stdout.split('\n')
        for line in lines[1:-1]:
            data[line.split()[-1]]=dict(zip(ITEM,line.split()))
        return data
    except:
        log.error("Can't get disk info.")
    
class Disk(checkScipt):
    def collector(self):
        diskinfo = getDisk()
        for instance in self.config['instance']:
            if diskinfo.has_key(instance['disk']):
                for item in instance['items']:
                    key = 'disk.'+instance['disk']+'.'+item
                    if diskinfo[instance['disk']].has_key(item):
                        value = diskinfo[instance['disk']][item]
                        self.add_guage(key,value)
        
# if __name__ == "__main__":

    # disk = Disk()
    # disk.debug()
    # print disk.getdataForm()
    
