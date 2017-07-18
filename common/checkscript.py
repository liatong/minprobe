from utils.config  import *
from socket import socket, AF_INET, SOCK_DGRAM
import yaml,imp
import glob
import inspect

log = logging.getLogger(__name__)

class checkScipt(object):
    def __init__(self,config=None,agentConfig=None):
        
        self.script_yaml = config 
        #get the config file same with the checkscript subclass name lower
        if self.script_yaml is None:
            self.script_yaml = self.__class__.__name__.lower()+'.yaml'
        if agentConfig is None:
            agentConfig = get_statsd_conf()
        self.agentConfig = agentConfig
        self.config = self.load_yaml_config()
        self.stclient = statsdClient(host=self.agentConfig['server'],port=self.agentConfig['port'])
        self.name = self.agentConfig['agent_name']
        
    def load_yaml_config(self):
        '''
        #Check the yaml config file,and return the yaml object like this.
        {'instance': [{'disk01': '/data', 'items': ['USE', 'FREE']}, {'items': ['USE'], 'disk02': '/'}], 'comman': None}
        '''
        config_path = get_script_conf_path()
        try:
            file = open(os.path.join(config_path,self.script_yaml),'r')
        except IOError:
            raise Exception("Can't read the check config file:%s" %self.script_yaml) 
        config = yaml.load(file)
        file.close()
        return config
     
    def add_timing(self,key,value):
        '''
        #Add defferent data type to statsd data form. such as: set,guage,time,etc. 
        '''
        self.stclient.timing('.'.join((self.name,key)),value)
    
    def add_set(self,key,value):
        '''
        #Add log set
        '''
        self.stclient.set('.'.join((self.name,key)),value)
    
    def add_guage(self,key,value):
        '''
        #add guage
        '''
        self.stclient.guage('.'.join((self.name,key)),value)
        
    def add_increment(self,key,value):
        '''
        #add increment
        '''
        self.stclient.increment('.'.join((self.name,key)),value)
    
    def collector(self):
        '''
        # collector data
        '''
        #subclass rewride the method
        pass
        
    def getdataForm(self):
        return self.stclient.getdata()
    
    def debug(self):
        self.collector()

    def run(self):
        '''
        #run()
        '''
        #do all work,like collector data and sent data to server.
        self.collector()
        self.stclient.send()
    
class statsdClient(object):
    SC_TIMING = "ms"
    SC_COUNT = "c"
    SC_GAUGE = "g"
    SC_SET = "s"
    
    def __init__(self,host='localhost',port=8125,protocal="UDP"):
        '''
        Send statistics to the statsd server daemon over UDP or TCP    
        '''
        self.addr = (host,port)
        self.protocal = protocal.upper()
        self.dataForm = []
    def timing(self,key,value):
        '''
        log timing information
        '''
        self.update_stats(key,value,self.SC_TIMING)
    
    def set(self,key,value):
        '''
        log set
        '''
        self.update_stats(key,value,self.SC_SET)
        
    def guage(self,key,value):
        '''
        log guages
        '''
        self.update_stats(key,value,self.SC_GAUGE)
    
    def increment(self,key,value):
        self.update_stats(key,value,self.SC_COUNT)
        
    def update_stats(self,keys,value,_type,sample_rate=1):
        '''
        Pipeline function that formats data,and append to dataForm.
        '''
        content = self.format(keys,value,_type)
        self.dataForm.extend(content.items())
        
    def format(self,keys,value,_type):
        '''
        General format function
        '''
        data = {}
        value = "{0}|{1}".format(value,_type)
        if not isinstance(keys,(list,tuple)):
            if keys.strip().__contains__(','):
                keys = map(lambda x:x.strip(),keys.strip().split(','))
            else:
                keys = keys.strip().split() 
        for key in keys:
            data[key] = value
        return data
    
    def getdata(self):
        return self.dataForm
    def resetData(self):
        self.dataForm=[]
        
    def send(self):
        '''
        Send key/value paint to statsd server via udp
        '''
        if self.protocal == "UDP":
            udp_sock = socket(AF_INET,SOCK_DGRAM)
            for data in self.dataForm:
                udp_sock.sendto(":".join(data).encode('utf-8'),self.addr)
                #log.info('Send to %s:%s  data:' %self.addr)
                self.resetData()

def check_yaml_config(config):
    return True
    
def load_checkscript(agentConfig=None,script_conf_path=None):
    '''
    Load the check script object from check_script path when script.conf  have script config file. like that check_disk.yaml. 
    '''
    #get path
    config_path = get_script_conf_path(agentConfig)
    if script_conf_path is None:
        script_path = get_script_path(agentConfig)
    if script_conf_path is not None and os.path.exists(script_conf_path):
        script_path = script_conf_path
        
    #Get the script file list that storage on script.d directory
    script_file_list = glob.glob(os.path.join(script_path,"*.py"))
    script_list = map(lambda x:os.path.basename(x).split('.')[0],script_file_list)

    #Get the config file list
    config_file_list = glob.glob(os.path.join(config_path,"*.yaml"))
    config_file_list = map(lambda x:os.path.basename(x),config_file_list)
    
    need_run_scripts = {}
    error_init_scripts = {}
    log.debug("Start load the script install from check_script path.")
    #Load the script obj from script module when have the config file with the script.
    log.debug("#config list is %s" %config_file_list)
    log.debug("#script lis is %s" %script_list)
    for config  in config_file_list:
    
        script = config.split('.')[0]
        if script not in script_list:
            log.error("Not have script %s.py with config file %s" %(script,config))
            continue
        
        if script in need_run_scripts:
            continue
            
        #check the config file
        config_status=False
        if check_yaml_config(os.path.join(config_path,config)):
            config_status=True
        
        if not config_status:
            log.error("Config file(%s) format is error,pls check it" %config) 
            continue
            
        #Load the check script module from the script path.
        try:
            #log.debug("module name is %s,path is %s" %(script.capitalize(),os.path.join(script_path,script+'.py')))
            check_module = imp.load_source("dni_%s" %script.capitalize(),os.path.join(script_path,script+'.py') )
        except:
            log.error("Can't load the module from the script file %s.py" %script) 
            continue
        
        classes = inspect.getmembers(check_module,inspect.isclass)
        for _,clsmember in classes:
            if clsmember == checkScipt:
                continue
            if issubclass(clsmember,checkScipt):
                check_class = clsmember
                if checkScipt in check_class.__bases__:
                    continue
                else:
                    break
        
        if not check_class:
            log.error("No check class is not subclass from checkScipt,pls check script file %s.py" %script) 
        try:
            script_obj = check_class(config=config,agentConfig=agentConfig)
            #Append the script obj to need_run_scripts, and it will be run.
            need_run_scripts[script]=script_obj
        except:
            log.error("Unable to initialize script %s" %script)
    
    ##return the need run script objects: dict
    return need_run_scripts
    


if __name__ == "__main__":
    init_logging()
    log = logging.getLogger()
    log.info("test!")
    name='memory'
    path='/data/DNIStatsd/script/memory.py'
    
    check_module = imp.load_source("dnit_%s" %name.capitalize(),path)
    print check_module
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    