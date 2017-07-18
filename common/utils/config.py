#lib
import os,sys
import ConfigParser
import logging,glob
import imp
import inspect
#
DEFAULT_CONF_NAME = "dnistatsd.conf"
DEFAULT_CONF_PATH = "/../../conf/"
AGENT_VERSION = "0.0.1"
DEFAULT_SCRIPT_PATH = "/../../script"
DEFAULT_STATSD_SERVER = '127.0.0.1'
DEFAULT_STATSD_PORT = 8125
DEFAULT_INTERVAL = 10
DEFAULT_SCRIPT_CONF_PATH = "/../../script_conf"
DEFAULT_AGENT_NAME = 'localhost'
DEFAULT_PIDFILE = '/var/run/dnistatsd.pid'
DEFAULT_LOGFILE = '/var/log/dnistatsd.log'

log = logging.getLogger(__name__)


def get_version():
    return AGENT_VERSION
    
def get_config_path(cfg_path=None):
    '''
    Get the config file real path. if config file is not exist will return None.
    '''
    if cfg_path is not None:
        return cfg_path if os.path.exists(cfg_path) else None
    try:
        path = os.path.realpath(__file__)
        path = os.path.dirname(path)+DEFAULT_CONF_PATH
        cfg_path = os.path.realpath(path+DEFAULT_CONF_NAME)
        return cfg_path if os.path.exists(cfg_path) else None
    except:
        pass
        
def get_config_dict():
    '''
    Load the dnistated.conf file option. Return the dict format data.
    '''
    path = get_config_path()
    if path is None:
        return None
    config = {}
    try:
        cf = ConfigParser.ConfigParser()    
        cf.read(path)
        if cf.has_option('Main','server'):
            config['server']=cf.get('Main','server')
        if cf.has_option('Main','listen_port'):
            config['port']=int(cf.get('Main','listen_port'))
        if cf.has_option('Main','default_interval'):
            config['default_interval']=int(cf.get('Main','default_interval'))
        if cf.has_option('Main','script_path'):
            config['script_path'] = cf.get('Main','script_path')
        if cf.has_option('Main','agent_name'):
            config['agent_name'] = cf.get('Main','agent_name')
        return config
    except:
        #log
        sys.stderr.wirte("Can not load config from the config file,pls check if have exits the config file %s" %path)

def get_pid_file(config=None):
    return config['pidfile'] if config.has_key('pidfile') else DEFAULT_PIDFILE
    
def get_log_file(config=None):
    return config['logfile'] if config.has_key('logfile') else DEFAULT_LOGFILE
    
def get_statsd_server(config=None):
    return config['server'] if config.has_key('server') else DEFAULT_STATSD_SERVER
        
def get_statsd_server_port(config=None):
    return config if config.has_key('listen_port') else DEFAULT_STATSD_PORT
    
def get_script_path(config=None):
    '''
    Get the default check script storage path. if script path is not exist will return None
    '''
    if isinstance(config,str):
        cfg_path = config
        
    elif isinstance(config,dict) and config.has_key('script_path'):
        cfg_path = config['script_path']
        
    else:
        try:
            path = os.path.dirname(os.path.realpath(__file__))
            cfg_path = os.path.realpath(path+DEFAULT_SCRIPT_PATH)
        except:
            pass
    return cfg_path if os.path.exists(cfg_path) else None
 
def get_script_conf_path(config=None):
    '''
    Get script config file directory.
    '''
    if config is not None and config.has_key('script_conf_path') and os.path.exist(config['script_conf_path']):
        return config['script_conf_path']
    else:
        path = os.path.dirname(os.path.realpath(__file__))
        cfg_path = os.path.realpath(path+DEFAULT_SCRIPT_CONF_PATH)
        return cfg_path
        
def get_check_interval(config=None):
    return config['check_interval'] if config.has_key('check_interval') else DEFAULT_INTERVAL
      
def get_agent_name(config=None):
    return config['agent_name'] if config.has_key('agent_name') else DEFAULT_AGENT_NAME

def init_logging():
    try:
        import logging
        DEFAULT_LOG_LEVEL = logging.INFO
        config = get_config_dict()
        DEFAULT_LOG_FILE = get_log_file(config)
        DEFAULT_LOG_FORMATTER = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    except:
        sys.stderr.write("Can't import logging modle!")
        sys.exit(1)
    global logger
    logger = logging.getLogger()
    #Add two handler one is echo to log file another is  print to stdout
    fileHandler = logging.FileHandler(DEFAULT_LOG_FILE)
    streamHandler = logging.StreamHandler()
    #Set logger  level
    logger.setLevel(DEFAULT_LOG_LEVEL)
    
    #Define the log formatter
    formatter = formatter = logging.Formatter(DEFAULT_LOG_FORMATTER)
    fileHandler.setFormatter(formatter)
    streamHandler.setFormatter(formatter)
    
    #logger add handerl
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)
  
def get_statsd_conf():
    '''
    Read statsd agent config from config path and return config(dict)
    '''
    
    config = get_config_dict()
    
    statsdConfig ={
        "version":get_version(),
        "server": get_statsd_server(config),
        "port": get_statsd_server_port(config),
        "script_path": get_script_path(config),
        "check_interval": get_check_interval(config),
        "script_conf": get_script_conf_path(config),
        "agent_name": get_agent_name(config),
    }
    
    return statsdConfig 



if __name__ == "__main__":
    init_logging()

    
    
    
    
    
