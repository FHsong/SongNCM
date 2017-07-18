#!/usr/bin/env python

import sys

sys.path.append('/home/song/PycharmProjects/SongNCM') # need add path at terminal

import logging
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from Tools.CreateTopology import SwitchHostLink

def createTopo():
    logging.debug("create 2 switch and 3 host")

    topo = SwitchHostLink(2, 3)
    topo.createTopo()
    topo.createLink(topo.switchlist[0], topo.hostlist[0])
    topo.createLink(topo.switchlist[0], topo.hostlist[1])
    topo.createLink(topo.switchlist[0], topo.switchlist[1])
    topo.createLink(topo.switchlist[1], topo.hostlist[2])

    controller_ip = "127.0.0.1"
    controller_port = 6633
    net = Mininet(topo=topo, link=TCLink, controller=None, autoSetMacs=True)
    net.addController('controller', controller=RemoteController,
                      ip=controller_ip, port=controller_port)
    net.start()

    # topo.open_service(net)

    CLI(net)
    net.stop()


if __name__ == '__main__':
    createTopo()
