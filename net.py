'''
Code Author: Peng, Caikun
File Name: net.py
Create Date: 16/07/2024 
Edited Date: 01/08/2024
Description: Start Mininet
Dependencies: mininet, math, json, os, subprocess
'''

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import Controller, OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info
import math
import json
import os
import subprocess

class IPv6DisabledSwitch(OVSSwitch):
    def start(self, controllers):
        super(IPv6DisabledSwitch, self).start(controllers)
        # close IPv6
        self.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
        self.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')

def get_white_list():
    try:
        whiteList = json.load(open('whitelist.json','r'))
    except Exception as e:
        whiteList = json.load(open('whitelist_default.json','r'))
    return whiteList

net = None
routingTable = {}

def setup_net(net):
    global routingTable
    if net is None:
        net = Mininet(
            link = TCLink, 
            switch = IPv6DisabledSwitch,
            controller = None,
            autoSetMacs = True, 
            autoStaticArp = True
        )

        net.addController(
            'Ctl0', 
            controller = RemoteController, 
            ip = '127.0.0.1', 
            port = 6653,
            protocols = "OpenFlow13"
        )

        dpidToSwitchName = {}
        # Number of devices
        numHosts = 4
        numSwitches = 2
        numMonitor  = 1
        numSwitchToHosts = math.ceil(numHosts / numSwitches)
        whiteList = get_white_list()
        numWeb = len(whiteList)
        
        # create monitor and links
        monitorDpid = f'{1:016x}'
        monitorName = f'm'
        monitor = net.addSwitch(monitorName, dpid = monitorDpid)
        info(f"Created monitor {monitorName} with DPID {monitorDpid}\n")
        routingTable[monitorDpid] = []
        dpidToSwitchName[monitorDpid] = [monitorName]

        for switchId in range(numSwitches): # create switch(es)
            switchDpid = f'{1:014x}{switchId+1:02x}'
            switchName = f's{switchId+1}'
            switch = net.addSwitch(switchName, dpid = switchDpid)
            info(f"Created switch {switchName} with DPID {switchDpid}\n")
            routingTable[switchDpid] = []
            dpidToSwitchName[switchDpid] = [switchName]
            # create link between monitor and switch
            linkMonitorToSwitch = net.addLink(switch, monitor)
            routingTable[monitorDpid].append({
                "cookie": "0x0",
                "priority": 10,
                'actions':[f'goto_table:{switchId+1}'],
                'match':{'ip,nw_dst': f'10.0.{switchId}.0/24'},
                "table": 0
            })
            routingTable[monitorDpid].append({
                "cookie": "0x0",
                "priority": 10,
                'actions':[f'output:{switchId+1}'],
                'match':{'ip,nw_dst': f'10.0.{switchId}.0/24'},
                "table": f'{switchId+1}'
            })
            routingTable[switchDpid].append({
                "cookie": "0x0",
                "priority": 1,
                'actions':['output:1'],
                'match':{},
                "table": 0
            })

            for hostId in range(numSwitchToHosts): # create host(s)
                hostIp = f'10.0.{switchId}.{hostId+2}' 
                hostName = f'h{switchId}{hostId}'
                host = net.addHost(hostName, ip = hostIp)
                # create link between switch and host
                linkHostToSwitch = net.addLink(host, switch)
                routingTable[switchDpid].append({
                    "cookie": "0x0",
                    "priority": 10,
                    'actions':[f'goto_table:{hostId+2}'],
                    'match':{'ip,nw_dst': hostIp},
                    "table": 0
                })
                routingTable[switchDpid].append({
                    "cookie": "0x0",
                    "priority": 10,
                    'actions':[f'output:{hostId+2}'],
                    'match':{'ip,nw_dst': hostIp},
                    "table": f'{hostId+2}'
                })

                # check the number of created host
                numHostCreated = switchId * numSwitchToHosts + hostId + 1
                if numHostCreated == numHosts:
                    break
        
        # create local server and white list webs
        server = net.addHost('localServer', ip = '10.0.0.1')
        linkMonitorToServer = net.addLink(server, monitor, intfName1='ls-eth0')
        routingTable[monitorDpid].append({
            "cookie": "0x0",
            "priority": 11,
            'actions':[f'goto_table:{numSwitches+1}'],
            'match':{'ip,nw_dst': '10.0.0.1'},
            "table": 0
        })
        routingTable[monitorDpid].append({
            "cookie": "0x0",
            "priority": 11,
            'actions':[f'output:{numSwitches+1}'],
            'match':{'ip,nw_dst': '10.0.0.1'},
            "table": f'{numSwitches+1}'
        })
        for webID in range(numWeb):
            webIP = whiteList[webID]['ip']
            webName = whiteList[webID]['name']
            web = net.addHost(f'{webName}', ip = webIP)
            linkMonitorToInternet = net.addLink(web, monitor)
            routingTable[monitorDpid].append({
                "cookie": "0x0",
                "priority": 10,
                'actions':[f'goto_table:{numSwitches+webID+2}'],
                'match':{'ip,nw_dst': webIP},
                "table": 0
            })
            routingTable[monitorDpid].append({
                "cookie": "0x0",
                "priority": 10,
                'actions':[f'output:{numSwitches+webID+2}'],
                'match':{'ip,nw_dst': webIP},
                "table": f'{numSwitches+webID+2}'
            })

        with open('routing_table.json', 'w') as file:
            json.dump(routingTable, file, indent = 2)
        with open('dpidToSwitchName.json', 'w') as file:
            json.dump(dpidToSwitchName, file, indent = 2)

    return net

def add_web(net):
    global routingTable
    whiteList = json.load(open('whitelist_add.json','r'))
    numWebDef = len(get_white_list())
    numWeb = len(whiteList)
    numSwitches = len(net.switches)-1
    monitor = net.get('m')
    monitorDpid = f'{1:016x}'
    for webID in range(numWeb):
        webIP = f"{whiteList[webID]['ip']}"
        webName = whiteList[webID]['name']
        web = net.addHost(f'{webName}', ip = webIP)
        linkMonitorToWeb = net.addLink(web, monitor)
        routingTable[monitorDpid].append({
            "cookie": "0x0",
            "priority": 10,
            'actions':[f'goto_table:{numSwitches+numWebDef+webID+2}'],
            'match':{'ip,nw_dst': webIP},
            "table": 0
        })
        routingTable[monitorDpid].append({
            "cookie": "0x0",
            "priority": 10,
            'actions':[f'output:{numSwitches+numWebDef+webID+2}'],
            'match':{'ip,nw_dst': webIP},
            "table": f'{numSwitches+numWebDef+webID+2}'
        })
    with open('routing_table_toadd.json', 'w') as file:
        json.dump(routingTable, file, indent = 2)
    with open('routing_table.json', 'w') as file:
        json.dump(routingTable, file, indent = 2)
    print('done')
    return net

def start_net(net):
    if net is not None:
        net.start()
        block_ipv6(net)
        print(f'start net: {net}')
    return net

def block_ipv6(net):
    for host in net.hosts:
        host.cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
        host.cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')
        host.cmd('sysctl -w net.ipv6.conf.lo.disable_ipv6=1')

def conf_net(net):
    global routingTable
    num_switches = len(net.switches)
    for switch in net.switches:
        switch_name = switch.name
        switch_dpid = switch.dpid
        for route in routingTable[switch_dpid]:
            add_flows(net,route,switch_name)
    return net

def cli_net(net):
    return CLI(net)

def get_net(net):
    print(net)
    return net

def stop_net(net):
    if net:
        net.stop()
        os.system("sudo mn -c")
    return net

def add_flows(net,route,switch_name):
    cookie = route['cookie']
    table = route['table']
    priority = route['priority']
    match = route['match']
    match_str = ",".join([f"{key}={value}" for key, value in match.items()])
    actions = ",".join(route["actions"])
    set_route = f'ovs-ofctl add-flow {switch_name} "cookie={cookie},table={table},priority={priority},{match_str},actions={actions}"'
    os.system(set_route)

if __name__ == '__main__':
    setLogLevel('info')
    net = None
    net = setup_net(net)
    ryu_process = subprocess.Popen(['xterm', '-e', 'ryu-manager switch.py ncm_api.py'])
    start_net(net)
    conf_net(net)
    cli_net(net)
    stop_net(net)
    ryu_process.terminate()
