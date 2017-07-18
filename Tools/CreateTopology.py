
from mininet.topo import Topo

class SwitchHostLink(Topo):
    switchlist = []
    hostlist = []

    def __init__(self, switchNum, hostNum, *args, **kwargs):
        super(SwitchHostLink, self).__init__(*args, **kwargs)
        self.switchNum = switchNum
        self.hostNum = hostNum

    def createTopo(self):
        self.createSwitch(self.switchNum)
        self.createHost(self.hostNum)


    def createSwitch(self, number):
        swparam = {'protocols': 'OpenFlow13'}
        for x in xrange(1, number + 1):
            self.switchlist.append(self.addSwitch("s" + str(x), **swparam))

    def createHost(self, number):
        for x in xrange(1, number + 1):
           self.hostlist.append(self.addHost("h"+str(x)))

    def createLink(self, node1, node2, port1=None, port2=None):
        self.addLink(node1, node2, port1=None, port2=None)

    def open_service(self, net):
        for i in range(len(self.hostlist) - 4):
            host = net.get(self.hostlist[i])
            host.popen(
                'iperf -s -p 8080 -u > log/server_' + str(host.IP()) + '_iperf_result.log', shell=True)
            if i in xrange(0, 4) or i in xrange(8, 12):
                host.popen(
                    'python -m SimpleHTTPServer 80', shell=True)
            if i in xrange(4, 8):
                host.popen(
                    'python -m pyftpdlib -p 21', shell=True)

