#!/usr/bin/env python
#init logging config
from common.utils.config import init_logging
init_logging()

import sys,time,os
from optparse import OptionParser  
sys.path.append(os.path.realpath(os.path.dirname(__file__)))

#project
from common.daemon import Daemon
from common.collecter import *
from common.checkscript import (
    get_version,
    load_checkscript,
)
from common.utils.config import (
    get_statsd_conf,
    get_config_dict,
    get_pid_file,
)

log = logging.getLogger('dnistatsd')

class DNIStatsd(Daemon):
    def __init__(self,pidfile):
        Daemon.__init__(self,pidfile)
        self.keep_running = True
        
    #Gracefully exit on sigterm.
    def _handler_sigterm(self,signum,frame):
        log.debug("Caught sigtem.Stoping keeping run")
        self.keep_running = False
    
    def run(self):

        #Get the dnistatsd agent's config from the dnistatsd.conf 
        statsdConfig = get_statsd_conf()
        
        #Load check script instance from path(/data/DNIStatsd/script),the script object like Disk(CheckScript)
        checksc_list = load_checkscript(agentConfig=statsdConfig)
        log.debug("Get the checksc_list is:%s" %checksc_list)
        
        
        #Check interval default is 10s
        check_interval = int(statsdConfig['check_interval'])
        
        #Collecter object loop run the script instance's  method run() to get data and send it.
        try:
            self.statsd = Collecter(agentConfig=statsdConfig,checkList=checksc_list)
        except:
            log.error("Can't instanse the Collector object!")
            sys.exit(2)
            
        while self.keep_running:
            log.debug("Run check script loop....")
            #Run statsd collector to get check_script data and send data to statsd(nodejs) server:port default is localhost:8085
            self.statsd.run()
            if self.keep_running:
                time.sleep(check_interval)
        try:
            #do something to clear status
            pass
        except Exception:
            pass
            
            
def get_args():
    '''
    Get option args
    '''
    parser = OptionParser(version=get_version())
    (options, args) = parser.parse_args()  
    return (options,args)
    
def main():
    options,args = get_args()
    COMMAND=[
        'start',
        'stop',
        'restart',
        'status',
    ]
    
    if len(args) < 1 or args[0].lower() not in COMMAND:
        sys.stderr.write("Usage: %s  %s\n" %(sys.argv[0],"|".join(COMMAND)))
        return 2

    command = args[0].lower()
    
    #get the pidfile path
    pidfile = get_pid_file(get_config_dict())
    
    #create a DNIStatsd install 
    dnistatsd = DNIStatsd(pidfile)
    
    #start the DNIStatsd
    if command == COMMAND[0]:
        log.info("Start the dnistatsd...")
        dnistatsd.start()
        
    #stop the DNIStatsd
    elif command == COMMAND[1]:
        log.info("Stop the dnistatsd....")
        dnistatsd.stop()
        
    #restart the DNIStatsd
    elif command == COMMAND[2]:
        log.info("Restart the dnistatsd....")
        dnistatsd.restart()
    elif command == COMMAND[3]:
        log.info("No support get status")
    
    return 0
        
if __name__ == "__main__":
    try:
        sys.exit(main())
    except:
        raise
