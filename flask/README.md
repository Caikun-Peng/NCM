# Flask Application Documentation

## Overview

This Flask application is designed to interact with an SDN (Software-Defined Networking) controller (RYU). 
It includes functionalities for user authentication, network switch and host management, 
and dynamic web page generation based on network topology.

## Key Features

1. **User Authentication**: Login and logout functionalities with user session management.
2. **Network Management**:
   - Fetch metwork topology and switch information.
   - Disconnect and reconnect all network devices.
   - Manage individual switches and hosts, including blocking, unblocking, and limiting bandwidth.
3. **Dynamic Page Generation**: Create web pages for each switch and host based on the network topology.
4. **Whitelist Management**: Read and write whitelist data for network devices.

## File Structure
``` markdown
flask/
├── app.py                     # The main Flask application file.
├── templates/                 # Directory containing HTML templates.
│   ├── login.html             # Template for the login page.
│   ├── home.html              # Template for the home page.
│   ├── cell_model.html        # Template for switch pages.
│   ├── host_model.html        # Template for host pages.
│   └── switch_pages/          # Directory containing dynamically generated switch and host pages.
│       ├── cell-1/            # Directory for switch 1 containing its related HTML files.
│       │   ├── switch.html    # cell page for switch 1.
│       │   ├── host-1.html    # Host 1 page for switch 1.
│       │   ├── host-2.html    # Host 2 page for switch 1.
│       │   └── ...  
│       ├── cell-2/            # Directory for switch 2 containing its related HTML files.
│       │   ├── switch.html    # cell page for switch 2.
│       │   ├── host-1.html    # Host 1 page for switch 2.
│       │   ├── host-2.html    # Host 2 page for switch 2.
│       │   └── ...
│       └── ...
...
```

## Setup

1. **Install Dependencies**: 

pip install flask
pip install flask-login
pip install flask-session
pip install requests

2. **Run the Application**:

python Flask_app.py

2. **Code Description**:

## Routes

### Authentication Routes

- **Login Route**: `/`
- **Methods**: `GET`, `POST`
- **Description**: Handles user login. On successful login, redirects to the home page.

- **Logout Route**: `/logout`
- **Methods**: `POST`
- **Description**: Logs out the current user and redirects to the login page.

### Home Routes

- **Home Route**: `/home`
- **Methods**: `GET`, `POST`
- **Description**: Displays the home page with switch information and whitelist data. 
  Allows navigation to individual switch pages.

### Network Management Routes

- **Disconnect All Devices**: `/disconnect`
- **Methods**: `POST`
- **Description**: Disconnects all network devices.

- **Reconnect All Devices**: `/reconnect`
- **Methods**: `POST`
- **Description**: Reconnects all network devices.

- **Whitelist Management**: `/whitelist`
- **Methods**: `POST`, `GET`
- **Description**: Updates the whitelist and restarts the network.

### Switch Management Routes

- **Switch Page**: `/switch_pages/<cell>/<filename>`
- **Methods**: `GET`, `POST`
- **Description**: Displays the page for a specific switch, including the hosts connected to it.

- **Disconnect Switch**: `/disconnectCell`
- **Methods**: `POST`
- **Description**: Disconnects a specific switch.

- **Reconnect Switch**: `/reconnectCell`
- **Methods**: `POST`
- **Description**: Reconnects a specific switch.

- **Get Flow Rules**: `/flow_rules`
- **Methods**: `GET`, `POST`
- **Description**: Fetches the flow rules for a specific switch.

### Host Management Routes

- **Disconnect Host**: `/disconnectHost`
- **Methods**: `POST`
- **Description**: Disconnects a specific host.

- **Limit Host Bandwidth**: `/limit_speed`
- **Methods**: `POST`
- **Description**: Limits the bandwidth for a specific host.

- **Reset Host**: `/restoreHost`
- **Methods**: `POST`
- **Description**: Resets the connection and bandwidth for a specific host.

- **Get Host Data Usage**: `/data_usage`
- **Methods**: `GET`, `POST`
- **Description**: Fetches the data usage for a specific host.

## Functions

### Network Interaction Functions

- **get_switches_hostsnum()**: Fetches the switch information and the number of hosts connected.
- **disconnection_rules()**: Disconnects all network devices.
- **reconnect_network()**: Reconnects all network devices.
- **read_whitelist()**: Reads the whitelist data from a file.
- **write_whitelist(data)**: Writes the whitelist data to a file.
- **switch_disconnection(cellid)**: Disconnects a specific switch.
- **switch_reconnection(cellid)**: Reconnects a specific switch.
- **get_flow_rules(cellid)**: Fetches the flow rules for a specific switch.
- **transform_flow_data(flow_table)**: Transforms flow table data into a readable format.
- **block_access(cellid, hostNo)**: Blocks a specific host.
- **unblock_host(cellid, hostNo)**: Unblocks a specific host.
- **limit_bandwidth(cellid, hostNo)**: Limits the bandwidth for a specific host.
- **reset_bandwidth(cellid, hostNo)**: Resets the bandwidth for a specific host.
- **get_usage(cellid, hostNo)**: Fetches the data usage for a specific host.

### Page Generation Functions

- **create_cell_host_pages(switches_hosts)**: 
  Creates dynamic web pages for each switch and host based on the network topology.

### Utility Functions

- **netRestart()**: Restarts the network.

## User Management

### User Class

- **User**: Represents a user with attributes for `id`, `name`, and `password`.

### Simulated User Database

- **users**: A list of `User` objects representing the simulated user database.

## Session Management

- **Session Configuration**: Configures the session to use the filesystem.
- **SECRET_KEY**: A secret key for session data to avoid CSRF attacks.

## Notes

- This application uses Flask-Login for user authentication and session management.
- Requests to the SDN controller are made using the `requests` library.
- The application dynamically generates web pages based on the network topology fetched from the SDN controller.

---

Feel free to reach out if you have any questions or need further assistance with the application!
