import logging
#
import os
import sys
import time
import atexit
from signal import SIGTERM

log = logging.getLogger(__name__)

class Daemon(object):
    '''
    A generic daemon class.
    
    Usage: subclass the Daemon and override the run() method 
    '''
    
    def __init__(self,pidfile,stdin=os.devnull,stdout=os.devnull,stderr=os.devnull):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        
    def daemonize(self):
        '''
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        '''
        
        try:
            pid = os.fork()
            if pid > 0:
                #exit first parent
                sys.exit(0)
        except OSError,e:
            sys.stderr.write("Fork #1 failed:%d (%s)\n"% (e.errno, e.strerror))
            sys.exit(1)
        
        os.chdir("/")
        os.setsid()
        os.umask(0)
        
        #Do second fork
        try:
            pid = os.fork()
            if pid > 0:
                #exit from second parent
                sys.exit(0)
        except OSError,e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1) 
        
        #redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin,'r')
        so = file(self.stdout,'a+')
        se = file(self.stderr,'a+',0)
        os.dup2(si.fileno(),sys.stdin.fileno())
        os.dup2(so.fileno(),sys.stdout.fileno())
        os.dup2(se.fileno(),sys.stderr.fileno())
        
        #write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" %pid)
        
    def delpid(self):
        os.remove(self.pidfile)
        
    def start(self):
        '''
        start the darmon
        '''
        #check for a pidfile to see if the daemon already runs 
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        if pid:
            message = "pidfile %s already exit.Daemon already running?\n"
            sys.stderr.write(message %self.pidfile)
            log.info(message %self.pidfile)
            sys.exit(1)
        #start the daemon
        log.info("The Daemon is running......")
        self.daemonize()
        self.run()

    
    def stop(self):
        '''
        stop the daemon
        '''
        #Get the pid from the pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
            
        if not pid:
            message = "pidfiel %s does not exit.Daemon not running?\n"
            sys.stderr.write(message %self.pidfile)
            log.info(message %self.pidfile)
        
        if pid:
            try:
                while 1:
                    os.kill(pid,SIGTERM)
                    time.sleep(0.1)
                log.info("The Daemon is stop......")
            except OSError,err:
                err = str(err)
                if err.find("No such process") > 0:
                    if os.path.exists(self.pidfile):
                        os.remove(self.pidfile)
                else:
                    print str(err)
                    sys.exit(1)
                    
                    
    def restart(self):
        '''
        restrt the daemon
        '''
        self.stop()
        self.start()
        
    def run(self):
        '''
        subclass should override this method.
        '''

#Test case         
class mydaemon(Daemon):
    def run(self):
        while True:
            time.sleep(10)
            log.info("my daemon is running")
            

if __name__ == "__main__":
    from utils.config import init_logging
    init_logging()
    daemon = mydaemon('/tmp/mydaemon.pid')
    if len(sys.argv) >=2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)