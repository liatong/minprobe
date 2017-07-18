import logging
log = logging.getLogger(__name__)

class Collecter(object):
    '''
    #Check colleter. run the check scirtpt list.
    '''
    def __init__(self,agentConfig=None,checkList=None):
        self.agentConfig = agentConfig
        self.checkList = checkList
        
    def run(self):
        #log.debug("The checklist is:%s" %self.checkList)
        if self.checkList:
            for name,script in self.checkList.items():
                try:
                    script.run()
                    #log.debug("Run the script (%s)" %name)
                except:
                    log.error("Error run the script %s"  %name)
        if self.checkList is None or len(self.checkList.items()) is 0:
            log.error( "Haven't script install at check_list, pls check the issue.")
    