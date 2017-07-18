from ryu.base import app_manager
from ryu.ofproto import ofproto_v1_3
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet, icmp


class ExampleSwitch(app_manager.RyuApp):
    """example switch"""
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
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
        print "add_flow"

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        print 'Packet-in'
        self.cout = self.cout + 1
        print self.cout


        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        # get datapath id to identify  which openflow switch
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})



        # store the information
        # parser and analysis the received packets
        pkt = packet.Packet(msg.data)
        pkt_eth = pkt.get_protocol(ethernet.ethernet)
        pkt_icmp = pkt.get_protocols(icmp.icmp)

        if len(pkt_icmp) != 0:
           pkt_icmp[0].data.data = 1234567890

        print 'pkt-------------', pkt
        print 'pkt_eth---------', pkt_eth
        print 'pkt_icmp--------', pkt_icmp
        print 'pkt_icmp_len----', len(pkt_icmp)
        if len(pkt_icmp) != 0:
            print (type(pkt_icmp[0]))
            print 'pkt_icmp[0]-----', pkt_icmp[0]

            print (type(pkt_icmp[0].data))
            print 'pkt_icmp[0]_data', pkt_icmp[0].data

            print 'pkt_icmp[0]_data_data', pkt_icmp[0].data.data




        dst = pkt_eth.dst
        src = pkt_eth.src

        in_port = msg.match['in_port']




        # learn a src mac address to avoid flood next time


        self.logger.info("packet in %s %s %s %s",dpid, src, dst, in_port)
        self.mac_to_port[dpid][src] = in_port
        print 'MAC---', self.mac_to_port




        # if the dst mac address has already learned
        # decide which port to send the packets, otherwise, flood
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
            print 'exit--exit'
        else:
            out_port = ofproto.OFPP_FLOOD
            print 'Flood--Flood'


        # construct actions
        actions = [ofp_parser.OFPActionOutput(out_port)]

        # install a flow mod msg
        if out_port != ofproto.OFPP_FLOOD:
            match = ofp_parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)

        # send a packet out
        out = ofp_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id, in_port=in_port,actions=actions)
        datapath.send_msg(out)
        print '\n'
