
Monitor solutions: agent+statsd+graphite. 
This tools is a client server agent that collect monitor info and send to statsd port.And then Statsd tools will send message to grephite.You can display graph from the graphite server.

It have some base script,you can use then just define the configure file that same the name for the scripte such as monitor network script  net.py and the configure file net.yaml.

You easy the developer the monitor script reference the demo.py and demo.yaml configure file.