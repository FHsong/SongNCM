#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.util import dumpNodeConnections

class MyTopo(Topo):
    def __init__(self):
        Topo.__init__(self)
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')
        host3 = self.addHost('h3')
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')

        self.addLink(host1, switch1)
        self.addLink(host2, switch1)
        self.addLink(host3, switch2)
        self.addLink(switch1, switch2)


topos={'mypopo': (lambda : MyTopo())}