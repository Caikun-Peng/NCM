# Webpage

The Project Webpage: [TELE4642 Project - Network Control and Monitoring](https://sites.google.com/view/tele4642-project-ncm)

# Basics 

## Topology
The topology of the network in this project is like:
``` markdown
┌──────┐      ╭─────────────────╮  REST API  ╭─────────────╮
│ Host ├──┐   | Ryu Controller  |<───────────| Application |
└──────┘  |   ╰────────╥────────╯            ╰──────┬──────╯
┌──────┐  |            ║                            | 
│ Host ├──┤   OpenFlow ╠═══════════════════════╗    |              ┌──────────┐
└──────┘  |            ║                       ║    |          ┌───┤ Internet |
┌──────┐  |       ┌────╨────┐           ┌──────╨────┴──────┐   |   └──────────┘
│ Host ├──┼───────┤ Switch  ├───────────┤ Monitor/Firewall ├───┤
└──────┘  |       └─────────┘           └─────────┬────────┘   |   ┌──────────────┐
          |                                       |            └───┤ Local Server |
 ......  ...                                      |                └──────────────┘
          |                                  ╭────┴────╮
┌──────┐  |                                  | Logger  |
│ Host ├──┘                                  ╰─────────╯
└──────┘  
```
where
- **Host**: Host node represents the terminal device in the network.
- **Switch**: Switch node connecta multiple hosts and manage traffic.
- **Monitor/Firewall**: Monitoring or firewall devices for network security and traffic monitoring.
- **Internet** and **Local Server**: Indicates the external Internet and local server.
- **Ryu Controller**: Controller communicates with the switch and monitor through the OpenFlow protocol.
- **Application**: Application sents REST API based information in ryu controller
- **Logger**: Logger records network activity logs (if necessary).

## Software versions
The versions of software used in this project are:

| Software | Version |
| -------- | ------- |
| Python   | 3.8.10  |
| Mininet  | 2.3.0   |
| Ryu      | 4.34    |

## REST API URL

URL used for APIs in this project
```
http://<controllerIP>:<controllerPort>/<field>/<devices>/<deviceID>/<name>
```

Get more information in [Wiki - REST API Documentation](https://github.com/Caikun-Peng/wiki/REST-API-Documentation)

# Scripts Description
## net.py

[This script](net.py) creates a network topo with IPv6 disabled switches and hosts.

Run script:
``` cmd 
python3 net.py
```

## ncm_api.py

