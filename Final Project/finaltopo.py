from mininet.net import Mininet
from mininet.log import lg, info
from mininet.cli import CLI
from mininet.node import Node
from mininet.link import Link
from mininet.topo import Topo
import os

class Mytopo(Topo):

    def __init__(self):
        global dic
        dic = {101: ['192.168.1.1',1000], 102: ['192.168.2.1', 2000], 103: ['192.168.3.1', 3000],
               201: ['192.168.1.2',1001], 202: ['192.168.2.2', 2001], 203: ['192.168.3.2', 3001],
               301: ['192.168.1.3',1002], 302: ['192.168.2.3', 2002], 303: ['192.168.3.3', 3002],
               401: ['192.168.4.2',4000], 402: ['192.168.4.1', 4001]}
        Topo.__init__(self)
        source = self.addHost('s', ip='192.168.4.3/24', defaultRoute='via 192.168.4.40',inNamespace = False)
        r1 = self.addHost( 'r1' , ip='192.168.4.2/24', defaultRoute= 'via 192.168.3.40', inNamespace = False)
        r2 = self.addHost( 'r2' , ip='192.168.1.3/24',defaultRoute= 'via 192.168.1.20',inNamespace = False)
        r3 = self.addHost('r3', ip='192.168.2.3/24',defaultRoute= 'via 192.168.2.20', inNamespace=False)
        r4 = self.addHost('r4', ip='192.168.3.3/24',defaultRoute= 'via 192.168.3.20', inNamespace = False)
        r5 = self.addHost('r5', ip='192.168.1.2/24',defaultRoute= 'via 192.168.1.10', inNamespace = False)
        r6 = self.addHost('r6', ip='192.168.2.2/24',defaultRoute= 'via 192.168.2.10', inNamespace = False)
        r7 = self.addHost('r7', ip='192.168.3.2/24',defaultRoute= 'via 192.168.3.10', inNamespace = False)

        h1 = self.addHost( 'h1' , ip='192.168.1.1/24', defaultRoute= 'via 192.168.5.50', inNamespace = False)
        h2 = self.addHost( 'h2' , ip='192.168.2.1/24', defaultRoute= 'via 192.168.2.50', inNamespace = False)
        h3 = self.addHost( 'h3' , ip='192.168.3.1/24', defaultRoute= 'via 192.168.3.50', inNamespace = False)

        info("Creating links\n")
        self.addLink(source, r1, intfName1='StoR1', params1 = {'ip':'192.168.4.2/24'},intfName2='R1toS', params2 = {'ip' : '192.168.4.1/24'})
        self.addLink(r1, r2,  intfName1 = 'R1toR2', params1 = {'ip': '192.168.1.3/24'},intfName2 = 'R2toR1', params2 = {'ip' : '192.168.4.20/24'})
        
        
        self.addLink(r2, r5, intfName1='R2toR5', params1 = {'ip':'192.168.1.2/24'}, intfName2= 'R5toR2', params2 = {'ip' : '192.168.1.3/24'})
        self.addLink(h1, r5, intfName1='H1toR5', params1 = {'ip': '192.168.1.2/24'},intfName2 = 'R5toH1', params2 = {'ip': '192.168.1.1/24'})
        self.addLink(r5, r6, intfName1='R5toR6', params1 = {'ip' : '192.168.2.2/24'}, intfName2='R6toR5',  params2 = {'ip' : '192.168.1.2/24'})
        
        
        self.addLink(r1, r3, intfName1='R1toR3',params1 = {'ip' : '192.168.2.3/24'}, intfName2='R3toR1',  params2 = {'ip' : '192.168.4.21/24'})
        
        
        self.addLink(r3, r6, intfName1='R3toR6', params1 = {'ip' : '192.168.2.2/24'},intfName2='R6toR3',  params2 = {'ip' : '192.168.2.3/24'})
        self.addLink(h2, r6, intfName2='R6toH2', params2={'ip' : '192.168.2.1/24'})
        self.addLink(r6, r7, intfName1='R6toR7',  params1 = {'ip' : '192.168.3.2/24'},intfName2='R7toR6', params2 = {'ip' : '192.168.2.2/24'})
        
        self.addLink(r1, r4, intfName1='R1toR4', params1 = {'ip' : '192.168.3.3/24'}, intfName2='r4-eth1', params2 = {'ip' : '192.168.4.22/24'} )
        
        
        
        self.addLink(r4, r7, intfName1='R4toR7', params1 = {'ip' : '192.168.3.2/24'}, intfName2='R7toR4', params2 = {'ip' : '192.168.3.3/24'} )
        self.addLink(h3, r7, intfName1='H3toR7', params1 = {'ip':'192.168.3.2/24'}, intfName2='R7toH3', params2={'ip': '192.168.3.1/24'})



        self.build()


def run():
    os.system=('mn -c')
    topo=Mytopo()
    net = Mininet(topo=topo)
    net.start()
    CLI(net)
    net.stop()

if __name__=='__main__':
    run()





