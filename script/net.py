# class Net(object):
    # pass
from common.checkscript import checkScipt
import logging,time

log = logging.getLogger(__name__)

def getNetStatus():
    data={}
    try:
        ifstat = open('/proc/net/dev').readlines()[2:]
        for stat in ifstat:
            data[stat.split()[0].split(':')[0]]=stat.split()[1:]
        return data
    except:
        log.debug("Can't read the /proc/net/dev file")
        
class Net(checkScipt):

    def collector(self):
        #print self.config
        #Get the tran bytes
        old = getNetStatus()
        time.sleep(0.99)
        new = getNetStatus()
        ##Get the net tranmite bytes interval 0.99s. default is Kb
        data={}
        for k in new:
            data[k]={}
            #Kb
            data[k]['INT']=round((int(new[k][0])-int(old[k][0]))/1024,3)
            data[k]['OUT']=round((int(new[k][8])-int(old[k][8]))/1024,3)
            
        #Get config and load the data  to checkScipt.dataForm
        for instance in self.config['instance']:
            device = instance['device']
            if data.has_key(device):
                for item in instance['items']:
                    self.add_guage('net.'+device+'.'+item,data[device][item])
        
# if __name__ == "__main__":
    # from common.utils.config import init_logging
    # init_logging()
    # import init_import
    # net = Net()
    # net.debug()
    # print net.getdataForm()
    