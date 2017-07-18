import unittest
import sys
import init_import
from common.utils.config  import *
from common.checkscript import *
from common.collecter import *
from script.memory import Memory
import logging

class testScript(object):
    def run(self):
       return True
       
class Disk(checkScipt):
    def collecter(self):
        self.add_timing('example1',2)
        self.add_set('example2',2)
        self.add_guage('example3',2)
        self.add_increment('example4',2)
        
class TestConfig(unittest.TestCase):

    def test_get_config_path_none(self):
        self.assertEqual(get_config_path("/tmp/data/nohave.conf"),None)
    
    def test_get_config_path_default(self):
        self.assertEqual(get_config_path(),"/data/DNIStatsd/conf/dnistatsd.conf")
    
    def test_get_script_path(self):
        self.assertEqual(get_script_path(),"/data/DNIStatsd/script")
    
    def test_get_script_path_error_none(self):
        self.assertEqual(get_script_path("/data/DNIStatsd/script1"),None)
    
    def test_get_config_dict(self):
        self.assertEqual(isinstance(get_config_dict(),dict),True)
    
    def test_get_config_dict_server(self):
        config = get_config_dict()
        self.assertEqual(config['server'],'172.17.92.141')
        self.assertEqual(config['port'],8125)
        #self.assertEqual(config['script_path'],'/data/DNIStatsd/script')
    
    def test_get_statsd_conf(self):
        statsd_config = get_statsd_conf()
        
    def test_get_script_conf_path(self):
        self.assertEqual(get_script_conf_path(),'/data/DNIStatsd/script_conf')
        
    def test_get_script_conf_path_config(self):
        config = get_config_dict()
        self.assertEqual(get_script_conf_path(config),'/data/DNIStatsd/script_conf')
    
    def test_get_pid_file(self):
        config = get_config_dict()
        self.assertEqual(get_pid_file(config),'/var/run/dnistatsd.pid')
        
    def test_log_file(self):
        config = get_config_dict()
        self.assertEqual(get_log_file(config),'/var/log/dnistatsd.log')
        
class TestStatsdClient(unittest.TestCase):
    
    def test_format(self):
        
        client = statsdClient()
        data=client.format('example1',12,'ms')
        self.assertEqual(data,{'example1':'12|ms'})
        
        data=client.format('example1,example2',12,'ms')
        self.assertEqual(data,{'example1':'12|ms','example2':'12|ms'})
        
        data=client.format('example1   ,example2',12,'ms')
        self.assertEqual(data,{'example1':'12|ms','example2':'12|ms'})
        
        data=client.format('example1   example2',12,'ms')
        self.assertEqual(data,{'example1':'12|ms','example2':'12|ms'})
        
    def test_add_value(self):
        client = statsdClient()
        client.timing('example1',2)
        client.set('example2',2)
        client.guage('example3',2)
        client.increment('example4',2)
        for data in client.dataForm:
            if data.__contains__('example1'):
                self.assertEqual(":".join(data),"example1:2|ms")
            if data.__contains__('example2'):
                self.assertEqual(":".join(data),"example2:2|s")
            if data.__contains__('example3'):
                self.assertEqual(":".join(data),"example3:2|g")
            if data.__contains__('example4'):
                self.assertEqual(":".join(data),"example4:2|c")
            
    def test_send_data(self):
        client = statsdClient(host='127.0.0.1',port=8085)
        client.timing('example1',2)
        client.set('example2',2)
        client.guage('example3',2)
        client.increment('example4',2)
        client.send()
    

class TestCheckScript(unittest.TestCase):
    
    def test_load_yaml_file(self):
        config={'instance': [{'disk': '/data', 'items': ['USE', 'FREE']}, {'items': ['USE','FREE','TOTAL'], 'disk': '/'}], 'comman': None}
        script = checkScipt(config="disk.yaml")
        yaml = script.load_yaml_config()
        self.assertEqual(yaml,config)
    
    def test_load_yaml_file_memory(self):
        script = checkScipt(config="memory.yaml")
        yaml = script.load_yaml_config()
        #print yaml
        
    # def test_checkScipt_class(self):
        # script = checkScipt(config='disk.yaml')
        # script.add_timing('example1',2)
        # script.add_set('example2',2)
        # script.add_guage('example3',2)
        # script.add_increment('example4',2)
        # dataForm = script.getdataForm()
        # for data in dataForm:
            # if data.__contains__('huadong.example1'):
                # self.assertEqual(":".join(data),"huadong.example1:2|ms")
            # if data.__contains__('huadong.example2'):
                # self.assertEqual(":".join(data),"huadong.example2:2|s")
            # if data.__contains__('huadong.example3'):
                # self.assertEqual(":".join(data),"huadong.example3:2|g")
            # if data.__contains__('huadong.example4'):
                # self.assertEqual(":".join(data),"huadong.example4:2|c")
            ##print data
            
    # def test_disk_checkScript_class(self):
       # disk = Disk()
       # disk.debug()
       # dataForm = disk.getdataForm()
       # for data in dataForm:
            # if data.__contains__('huadong.example1'):
                # self.assertEqual(":".join(data),"huadong.example1:2|ms")
            # if data.__contains__('huadong.example2'):
                # self.assertEqual(":".join(data),"huadong.example2:2|s")
            # if data.__contains__('huadong.example3'):
                # self.assertEqual(":".join(data),"huadong.example3:2|g")
            # if data.__contains__('huadong.example4'):
                # self.assertEqual(":".join(data),"huadong.example4:2|c")
        
    def test_checkScipt_send(self):
        memory = Memory()
        memory.debug()
        memory.run()
                
class TestLoadCheck(unittest.TestCase):

    def test_load_checkscript(self):
        need_check = load_checkscript()
        print need_check

class TestCollecter(unittest.TestCase):

    def test_collecter(self):
        sc = testScript()
        sc_list = {'disk':sc}
        colleter = Collecter(checkList=sc_list)
        colleter.run()
        
    def test_collector_scriptlit_nulldict(self):
        statsdConfig = get_statsd_conf()
        checksc_list = {}
        statsd = Collecter(agentConfig=statsdConfig,checkList=checksc_list)
        statsd.run()

        
if __name__ == "__main__":
    init_logging()
    unittest.main()
