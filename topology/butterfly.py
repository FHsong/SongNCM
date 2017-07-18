#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.util import dumpNodeConnections

class MyTopo(Topo):
    def __init__(self):
        Topo.__init__(self)


        switch1 = self.addSwitch('s1', mac = '00:00:00:00:00:01')
        switch2 = self.addSwitch('s2', mac = '00:00:00:00:00:02')
        switch3 = self.addSwitch('s3', mac = '00:00:00:00:00:03')
        switch4 = self.addSwitch('s4', mac = '00:00:00:00:00:04')
        switch5 = self.addSwitch('s5', mac = '00:00:00:00:00:05')
        switch6 = self.addSwitch('s6', mac = '00:00:00:00:00:06')
        switch7 = self.addSwitch('s7', mac = '00:00:00:00:00:07')

        host1 = self.addHost('h1', mac = '10:00:00:00:00:01')
        host2 = self.addHost('h2', mac = '10:00:00:00:00:02')
        host3 = self.addHost('h3', mac = '10:00:00:00:00:03')
        host4 = self.addHost('h4', mac = '10:00:00:00:00:04')
        host5 = self.addHost('h5', mac = '10:00:00:00:00:05')
        host6 = self.addHost('h6', mac = '10:00:00:00:00:06')
        host7 = self.addHost('h7', mac = '10:00:00:00:00:07')


        self.addLink(host1, switch1)
        self.addLink(host2, switch2)
        self.addLink(host3, switch3)
        self.addLink(host4, switch4)
        self.addLink(host5, switch5)
        self.addLink(host6, switch6)
        self.addLink(host7, switch7)


        self.addLink(switch1, switch2)
        self.addLink(switch1, switch3)
        self.addLink(switch2, switch6)
        self.addLink(switch3, switch7)
        self.addLink(switch2, switch4)
        self.addLink(switch3, switch4)
        self.addLink(switch4, switch5)
        self.addLink(switch5, switch6)
        self.addLink(switch5, switch7)

topos = {'butterfly': (lambda: MyTopo())}
