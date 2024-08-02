# Webpage

The Project Webpage: [TELE4642 Project - Network Control and Monitoring](https://sites.google.com/view/tele4642-project-ncm)

# Quick Start
## Start system
To start NCM system, only run script `run.py`. Ensure running as administer.

``` bash
sudo python3 run.py
```

## Dashboard
NCM support using dashboard to control the system.

Open the url: `http://localhost:5000/` in any browser.

``` bash
xdg-open http://localhost:5000/
```



# Basics 

## Topology
The topology of the network in this project is like:
``` markdown
┌──────┐      ╭─────────────────╮  REST API  ╭─────────────╮
│ Host ├──┐   | Ryu Controller  |<───────────| Application |
└──────┘  |   ╰────────╥────────╯            ╰──────┬──────╯
┌──────┐  |            ║                            | 
│ Host ├──┤   OpenFlow ╠═══════════════════════╗    |              ┌───────────────────────┐
└──────┘  |            ║                       ║    |          ┌───┤ Whitelisting websites |
┌──────┐  |       ┌────╨────┐           ┌──────╨────┴──────┐   |   └───────────────────────┘
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
- **Internet websites** and **Local Server**: Other _hosts_ simulated as internet webs and local server
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
| Flask    | 3.0.3   |

## REST API 

NCM support RESTful API, including `GET`, `PUT`, `POST`, and `DELETE`.

Get more information in [Wiki - REST API Documentation](https://github.com/Caikun-Peng/NCM/wiki/REST-API-Documentation)

# Scripts Description
## run.py

Run [this script](run.py) to start the ncm system. 

``` bash
sudo python3 run.py
```

## net.py

[This script](net.py) creates a network topo with IPv6 disabled switches and hosts.

Run script:
``` bash 
sudo python3 net.py
```

## ncm_api.py

[This script](ncm_api.py) defines the API interfaces.

Run script:
``` bash 
ryu-manager ncm_api.py
```

## flask/Flask_app.py 

[This script](flask/Flask_app.py) designs functionalities for user authentication, network switch and host management, 
and dynamic web page generation based on network topology.

Run script:
``` bash
cd flask
python3 Flask_app.py
```

Get more information in [flask page](flask/README.md).