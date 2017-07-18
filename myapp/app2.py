from ryu.base import app_manager
from ryu.ofproto import ofproto_v1_3, ether
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet, arp
import array


class ExampleSwitch(app_manager.RyuApp):
    """example switch"""
    OFP_VERIONS = [ofproto_v1_3.OFP_VERSION]
    def __init__(self, *args, **kwargs):
        super(ExampleSwitch, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.cout=0

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        # install the table-miss flow entry
        match = ofp_parser.OFPMatch()
        actions = [ofp_parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                              ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        print "switch_features_handler"


    def add_flow(self, datapath, priority, match, actions):
        # add a flow enery and install it into datapath
        ofproto = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        # construct a flow_mod msg and sent it
        inst = [ofp_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                                 actions)]
        mod = ofp_parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        e = ethernet.ethernet(dst='ff:ff:ff:ff:ff:ff',
                              src='08:60:6e:7f:74:e7',
                              ethertype=ether.ETH_TYPE_ARP)
        a = arp.arp(hwtype=1, proto=0x0800, hlen=6, plen=4, opcode=2,
                    src_mac='08:60:6e:7f:74:e7', src_ip='192.0.2.1',
                    dst_mac='00:00:00:00:00:00', dst_ip='192.0.2.2')
        p = packet.Packet()
        p.add_protocol(e)
        p.add_protocol(a)

        p.data = 0000
        p.serialize()

        print repr(p.data)
