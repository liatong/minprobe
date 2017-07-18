import init_import
from common.checkscript import checkScipt
import logging,time

log = logging.getLogger(__name__)


try:
    from kafka import KafkaConsumer,KafkaProducer
except:
    log.error("Can't no import kafka moduler.")

def toConsumer(server,topic,groupid='monitor'):
    data = {}
    try:
        consumer = KafkaConsumer(topic,group_id=groupid,bootstrap_servers=server,consumer_timeout_ms=1000,enable_auto_commit=True)
        for message in consumer:
            pass
        data['offset'] = message.offset
        data['message'] = message.value
        data['status'] = 1
        consumer.close()
    except:
        log.error("Consumer can get message from server.")
        data['status'] = 0
    
    return data
    
    
def toProducer(server,topic):
    data = {}
    try:
        producer = KafkaProducer(bootstrap_servers=server)
        message = time.asctime()
        future = producer.send(topic,message)
        record_metadata = future.get(timeout=10)
        data['topic'] = record_metadata.topic
        data['offset'] = record_metadata.offset
        data['partition'] = record_metadata.partition
        data['status'] = 1
        data['message'] = message
        producer.flush()
    except:
        log.error("Producer can send message")
        data['status'] = 0
    
    return data
    
def monitorResult(**kwargs):
    data = {}
    server = kwargs['server'].split(',')
    topic = kwargs['topic']
    port = kwargs['port']
    groupid = kwargs['groupid']
    serverList = map(lambda x:x+':'+str(port),server)
    
    pdata = toProducer(serverList,topic)
    time.sleep(1)
    cdata = toConsumer(serverList,topic,groupid)
    #print 'cdata',cdata
    #print 'pdata',pdata
    if cdata['status'] == pdata['status'] == 1 and cdata['offset'] == pdata['offset'] :
        data['offset'] = cdata['offset']
    data['status'] = cdata['status']
    return data
    
class kafkacluster(checkScipt):
    def collector(self):
        print self.config
        for instance in self.config['instance']:
            print monitorResult(**instance)
        
if __name__ == "__main__":
    from common.utils.config import init_logging
    init_logging()
    import init_import
    ps = kafkacluster()
    ps.debug()
    print ps.getdataForm()
