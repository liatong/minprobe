import init_import
from common.checkscript import checkScipt
import logging,time

log = logging.getLogger(__name__)
try:
    import urllib2
except:
    log.error("Can't load urlllib2 module.")
    
def getwebstatus(server,url='/',respon=None):
    print server,url,respon
    data ={}
    try:
        http = urllib2.urlopen('http://'+server+'/'+url)
        result = http.read()
        code = http.getcode()
        
        if code == 200 and respon is None:
            data['status'] = 1
        elif code == 200 and result == respon :
            data['status'] = 1
        else:
            print result == respon
            data['status'] = 0
        data['code'] = code
    except:
        data['status'] = 0
        data['code'] = 404
        
    return data
    
class Web(checkScipt):

    def collector(self):
        server = self.config['comman']['server']
        for instance in self.config['instance']:
            url = instance['url']
            if instance['items'].has_key('respon'):
                respon = instance['items']['respon']
            else:
                respon = None 
            data = getwebstatus(server,url,respon)
            #print data
            self.add_guage('web.'+server.replace('.','_')+'.'+url.replace('.','_')+'.status',data['status'])
            self.add_guage('web.'+server.replace('.','_')+'.'+url.replace('.','_')+'.code',data['code'])
            
if __name__ == "__main__":
    from common.utils.config import init_logging
    init_logging()
    import init_import
    ps = Web()
    ps.debug()
    print ps.getdataForm()