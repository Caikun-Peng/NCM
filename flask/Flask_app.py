from flask import Flask, request, session, redirect, send_from_directory
from flask import jsonify, render_template, flash, url_for
import requests
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
import re
import os
import shutil
from flask_session import Session
import json
# Initialize Flask application
app = Flask(__name__)
# RYU_CONTROLLER_URL = 'http://127.0.0.1:8080'
app.config['SECRET_KEY'] = '3tele!People4642' # Secret_key for session data; avoid CSRF attack
app.config['SESSION_TYPE'] = 'filesystem' # Configure the session to use the filesystem
Session(app)
TEMPLATE_DIR = os.path.join(os.getcwd(), 'templates') # Define the templates directory

# ==========================================================================================
#region Interact with ryu
# ========In home page=======
#region home page
# get switch dpid and number of ports connected to hosts
def get_switches_hostsnum():
    try:
        response = requests.get('http://127.0.0.1:8080/topo/switches')
        response.raise_for_status()  # Check if the request was successful
        switches = response.json()  # Convert response data to JSON format
        switches_dpid_hosts_list = []  # List to store dpid and port_no pairs
        
        for switch in switches:
            dpid = switch['dpid']
            int_dpid = int(dpid, 16)
            if int_dpid >= 0x100:  # Compare with hexadecimal 100
                port_count = len(switch['ports']) - 1 # One port is connected to monitor
                switches_dpid_hosts_list.append((dpid, port_count))         
        return switches_dpid_hosts_list
    except requests.exceptions.RequestException as e:
        flash(f'Error fetching switches: {e}')
        return None
# Block all network. Put rules to block all hosts from net
def disconnection_rules(): 
    try:
        response = requests.delete('http://127.0.0.1:8080/flow/switches')
        response.raise_for_status()
        flash('Successful Disconnection')
        print("Disconnection successful")
    except requests.exceptions.RequestException as e:
        flash(f'Error disconnection: {e}')
        print(f"Error disconnection: {e}")
# Delete block rules
def reconnect_network(): 
    try:
        response = requests.delete('http://127.0.0.1:8080/flow/deleted')
        print(response)
        response.raise_for_status()
        flash('Successful Connection')
        print("Connection successful")
    except requests.exceptions.RequestException as e:
        flash(f'Error connection: {e}')
        print(f"Error connection: {e}")

def read_whitelist():
    whitelist_file = os.path.join(os.path.abspath(os.path.dirname(app.root_path)), 'whitelist.json')
    if os.path.exists(whitelist_file):
        with open(whitelist_file, 'r') as f:
            return json.load(f)
    return []
def write_whitelist(data):
    filepath = os.path.join(os.path.abspath(os.path.dirname(app.root_path)), 'whitelist_to_add.json')
    print(os.path.dirname(app.root_path))
    print('data:',data,type(data))
    table = []
    for item in data:
        web = {}
        if item['block'] == 'Y':
            web['name']=item['name']
            web['ip']=item['ip']
            table.append(web)
    
    with open(filepath, 'w') as f:
        json.dump(table, f, indent=4)
# # Update whitelist according to the data from web
# def update_whitelist(whitelist):
#     for list in whitelist:
#         if list.action == True:
#         elif list.action == False:
#         else:

    
#     try:
#         response = requests.put('http://127.0.0.1:8080/flow/switches')
#         response.raise_for_status()

#endregion

# ========In one cell========
#region cell page
# Block one switch. Put rules to block hosts in one cells
def switch_disconnection(cellid): 
    try:
        dpid = cellid + 256
        response = requests.delete(f'http://127.0.0.1:8080/flow/switches/{dpid}')
        print(response)
        response.raise_for_status()
        flash('Successful Disconnection')
        print("Disconnection successful")
    except requests.exceptions.RequestException as e:
        flash(f'Error disconnection: {e}')
        print(f"Error disconnection: {e}")
# Reconnect network for one cell/switch
def switch_reconnection(cellid):  
    try:
        dpid = cellid + 256  
        response = requests.delete(f'http://127.0.0.1:8080/flow/deleted/{dpid}')
        response.raise_for_status()
        flash('Successful Connection')
        print("Connection successful")
    except requests.exceptions.RequestException as e:
        flash(f'Error connection: {e}')
        print(f"Error connection: {e}")
# Get flow table from current switch
def get_flow_rules(cellid):
    try:
        # dpid = f'{cellid + 256:x}'  # Convert dpid to hexadecimal string
        dpid = cellid + 256  # Convert dpid to hexadecimal string
        response = requests.get(f'http://127.0.0.1:8080/flow/switches/{dpid}')
        response.raise_for_status()
        flowrules = response.json()
        return flowrules
    except requests.exceptions.RequestException as e:
        flash(f'Error get flow rules: {e}')
        return None
def transform_flow_data(flow_table):
    transformed_data = []
    
    for switch in flow_table:
        dpid = switch.get('dpid')
        flows = switch.get('flows', [])
        
        for flow in flows:
            priority = flow.get('priority')
            match = ', '.join([f"{key}:{value}" for key, value in flow.items() if key.startswith('ip') or key.startswith('nw')])
            action = flow.get('actions')
            
            transformed_data.append({
                'Priority': priority,
                'MATCH': match,
                'ACTION': action
            })
    
    return transformed_data

#endregion

# ========In one host========
#region host page
# Block access from switch
def block_access(cellid, hostNo):
    try:
        # dpid = f'{cellid + 256:x}'  # Convert dpid to hexadecimal string
        dpid = cellid + 256
        portNo = hostNo + 1

        # # Define the URL
        # url = f'http://127.0.0.1:8080/flow/switches/{dpid}/{portNo}'
        
        # # Define the data payload
        # data = {
        #     "cookie": "0xf",
        #     "table": 0,
        #     "priority": 65535, # Priority for block rules
        #     "match": {
        #         "in_port": portNo
        #     },
        #     "actions": []
        # }
        
        # response = requests.put(url, json=data)

        response = requests.delete(f'http://127.0.0.1:8080/flow/switches/{dpid}/{portNo}')
        response.raise_for_status()
        print('True')
        flash('Successfully Blocked')
        print("Blocked Successfully")
    except requests.exceptions.RequestException as e:
        flash(f'Error blocked: {e}')
        print(f"Error blocked: {e}")

# Limit Bandwidth to 1MB/s, burst 0.1MB/s
def limit_bandwidth(cellid, hostNo):
    try:
        print('limit_bandwidth')
        dpid = f'{cellid + 256}' 
        portNo = hostNo + 1

        url = f'http://127.0.0.1:8080/rate/switches/{dpid}/{portNo}'
        print(url)
        data = {
            "rate": "8000",
            "burst": "100"   # "rate": 8 Mbps -> 1MB/s ,"burst": 0.1 MB/s
        }
        print(data)
        response = requests.put(url, json=data)
        print(response)
        response.raise_for_status()
        flash('Bandwidth Limited Successfully')
        print("Bandwidth Limited Successfully")
        return data
    except requests.exceptions.RequestException as e:
        flash(f'Error limiting bandwidth: {e}')
        print(f"Error limiting bandwidth: {e}")
# Unlimit bandwidth
def reset_bandwidth(cellid, hostNo):
    try:
        dpid = f'{cellid + 256}'  
        portNo = hostNo + 1

        url = f'http://127.0.0.1:8080/rate/switches/{dpid}/{portNo}'
        data = {
            "rate": "0",
            "burst": "0"
        }
        response = requests.put(url, json=data)
        
        response.raise_for_status()
        flash('Reset Successfully')
        print("Reset Successfully")
    except requests.exceptions.RequestException as e:
        flash(f'Error reseting bandwidth: {e}')
        print(f"Error reseting bandwidth: {e}")

# Get Usage of one host 
def get_usage(cellid, hostNo):
    try:
        # dpid = f'{cellid + 256:x}'  # Convert dpid to hexadecimal string
        dpid = cellid + 256
        portNo = hostNo + 1
        url = f'http://127.0.0.1:8080/flow/switches/{dpid}/{portNo}'
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        flow_table = response.json()  # Convert response data to JSON format

        return flow_table
    except requests.exceptions.RequestException as e:
        flash(f'Error reseting bandwidth: {e}')
        print(f"Error reseting bandwidth: {e}")
        return None
#endregion

#endregion
# ==========================================================================================


def create_cell_host_pages(switches_hosts):
    # Clean up files
    current_dir = os.path.join(TEMPLATE_DIR, 'switch_pages')
    if os.path.exists(current_dir):
        for filename in os.listdir(current_dir):
            if filename.startswith('cell-'):
                file_path = os.path.join(current_dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')

    # # Read index.html template content
    # index_template_path = os.path.join(TEMPLATE_DIR, 'switch_pages', 'index.html')
    # with open(index_template_path, 'r') as template_file:
    #     template_content = template_file.read()  
    
    with app.app_context():
    # Create files and directories
        for i in range(len(switches_hosts)):
            switch_dir = os.path.join(current_dir, f'cell-{i+1}')  # Path to the switch directory
            os.makedirs(switch_dir, exist_ok=True)  # Create the switch directory if it doesn't exist
            
            # Render template with dynamic data
            portNum = switches_hosts[i][1]
            switch_content = render_template('cell_model.html', num=portNum, iii=i+1)
            
            # Create switch.html file in the newly created directory
            switch_file_path = os.path.join(switch_dir, 'switch.html')
            with open(switch_file_path, 'w') as switch_file:
                switch_file.write(switch_content)

            
            # Create host pages
            for j in range(int(portNum)):
                host_content = render_template('host_model.html', iii = i+1, jjj= j+1)
                host_file_path = os.path.join(switch_dir, f'host-{j+1}.html')
                with open(host_file_path, 'w') as host_file:
                    host_file.write(host_content)



# ======================================================================
#region Deal with message from web
# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class to simulate database with in-memory storage
class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

# Simulate a user database
users = [User(id=1, name='user1', password='Password1!')]

# # Add admin
# class User(UserMixin):
#     def __init__(self, id, name, password, is_admin=False):
#         self.id = id
#         self.name = name
#         self.password = password
#         self.is_admin = is_admin
# users = [
#     User(id=1, name='user1', password='Password1!'),
#     User(id=2, name='admin', password='AdminPass1!', is_admin=True)  # Admin user
# ]


# Load user function
@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None


# Route for login page and form handling
@app.route('/', methods=['GET', 'POST'])
def login():
    # Check if 'switches_hosts' is not in the session, then fetch the data
    if 'switches_hosts' not in session:
        session['switches_hosts'] = get_switches_hostsnum()
    # If form data is submitted
    if request.method == 'POST':
        
        # Get form data
        name = request.form.get('username')
        password = request.form.get('password')
        print(name)
        print(password)

        # Perform basic form data validation        
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            flash('Invalid password. It should be at least 8 characters long and include at least one letter, one number, and one special character.')
            return render_template('login.html')

        # Authenticate users and passwords
        print('true')
        user = next((u for u in users if u.name == name and u.password == password), None)
        if user:
            print('2')
            login_user(user)
            # if user.is_admin:
            #     return redirect('/admin_home')
            # else:
            #     return redirect('/home')
                    # Check if 'switches_hosts' is not in the session, then fetch the data
            # if 'switches_hosts' not in session:
            session['switches_hosts'] = get_switches_hostsnum()
            
            print(session['switches_hosts'])
            return redirect('/home')
        else:
            flash('Invalid username or password.')
            return render_template('login.html')

    return render_template('login.html')


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')

# home buttones===============================
@app.route('/disconnect', methods=['POST'])
@login_required
def disconnect_all():
    if request.method == 'POST':
        disconnection_rules()
        # return redirect(url_for('home'))
    # return render_template('home.html', N = Num_switches)
    # return redirect('/home')
        return jsonify({'message': 'All devices disconnected successfully'})

@app.route('/reconnect', methods=['POST'])
@login_required
def reconnect_all():
    reconnect_network()
    return jsonify({'message': 'All devices reconnected successfully'})

@app.route('/whitelist', methods=['POST','GET'])
def whitelist_1():
    new_data = request.json
    write_whitelist(new_data)
    netRestart()
    return redirect('/home')

# @app.route('/restart', methods=['POST'])
def netRestart():
    response = requests.post('http://127.0.0.1:8080/net/restart')


# cell buttones===============================
@app.route('/disconnectCell', methods=['POST'])
@login_required
def disconnect_cell():
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return jsonify({'message': 'No JSON data provided'}), 400
        
        cell_id = int(data)
        if cell_id is None:
            return jsonify({'message': 'Cell ID is missing'}), 400
        
        try:
            switch_disconnection(cell_id)
            return jsonify({'message': f'Cell {cell_id} disconnected successfully'})
        except Exception as e:
            return jsonify({'message': f'Failed to disconnect cell {cell_id}: {e}'}), 500

@app.route('/reconnectCell', methods=['POST'])
@login_required
def reconnect_cell():
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return jsonify({'message': 'No JSON data provided'}), 400
        
        cell_id = int(data)
        if cell_id is None:
            return jsonify({'message': 'Cell ID is missing'}), 400
        
        try:
            switch_reconnection(cell_id)
            return jsonify({'message': f'Cell {cell_id} reconnected successfully'})
        except Exception as e:
            return jsonify({'message': f'Failed to reconnect cell {cell_id}: {e}'}), 500


@app.route('/flow_rules', methods=['GET', 'POST'])
@login_required
def flow_ru1e():
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return jsonify({'message': 'No JSON data provided'}), 400
        cell_id = int(data)
        if cell_id is None:
            return jsonify({'message': 'Cell ID is missing'}), 400
        
        try:
            flow_table = get_flow_rules(cell_id)
            new_flow = transform_flow_data(flow_table)
            # print(f'flow_table\n{flow_table}')
            print(new_flow)
            return new_flow
        except Exception as e:
            return jsonify({'message': f'Failed to reset cell {cell_id} : {e}'}), 500
# host buttones===============================
@app.route('/disconnectHost', methods=['POST'])
@login_required
def disconnect_host():
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return jsonify({'message': 'No JSON data provided'}), 400
        cell_data = data.get('data1')
        cell_id = int(cell_data)
        host_data = data.get('data2')
        host_id = int(host_data)
        if cell_id is None:
            return jsonify({'message': 'Cell ID is missing'}), 400
        if host_id is None:
            return jsonify({'message': 'Cell ID is missing'}), 400
        
        try:
            block_access(cell_id, host_id)
            return jsonify({'message': f'Cell {cell_id} Host {host_id} disconnected successfully'})
        except Exception as e:
            return jsonify({'message': f'Failed to disconnect cell {cell_id}  Host {host_id}: {e}'}), 500

@app.route('/limit_speed', methods=['POST'])
@login_required
def limit_band():
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return jsonify({'message': 'No JSON data provided'}), 400
        cell_data = data.get('data1')
        cell_id = int(cell_data)
        host_data = data.get('data2')
        host_id = int(host_data)
        if cell_id is None:
            return jsonify({'message': 'Cell ID is missing'}), 400
        if host_id is None:
            return jsonify({'message': 'Cell ID is missing'}), 400
        
        try:
            d = limit_bandwidth(cell_id, host_id)
            return jsonify({'message': f'Cell {cell_id} Host {host_id} Data {d} Limit bandwidth successfully'})
        except Exception as e:
            return jsonify({'message': f'Failed to limit bandwidth of cell {cell_id}  Host {host_id}: {e}'}), 500
        

@app.route('/restoreHost', methods=['POST'])
@login_required
def reset_host():
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return jsonify({'message': 'No JSON data provided'}), 400
        cell_data = data.get('data1')
        cell_id = int(cell_data)
        host_data = data.get('data2')
        host_id = int(host_data)
        if cell_id is None:
            return jsonify({'message': 'Cell ID is missing'}), 400
        if host_id is None:
            return jsonify({'message': 'Cell ID is missing'}), 400
        
        try:
            reset_bandwidth(cell_id, host_id)
            return jsonify({'message': f'Cell {cell_id} Host {host_id} reset successfully'})
        except Exception as e:
            return jsonify({'message': f'Failed to reset cell {cell_id}  Host {host_id}: {e}'}), 500
        
@app.route('/data_usage', methods=['GET', 'POST'])
@login_required
def data_usage():
    print('data_usage')
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            print('None')
            return jsonify({'message': 'No JSON data provided'}), 400
        cell_data = data.get('data1')
        cell_id = int(cell_data)
        host_data = data.get('data2')
        host_id = int(host_data)
        if cell_id is None:
            print(cell_id)
            return jsonify({'message': 'Cell ID is missing'}), 400
        if host_id is None:
            print(host_id)
            return jsonify({'message': 'Cell ID is missing'}), 400
        
        try:
            flow_table = get_usage(cell_id, host_id)
            print(f'flow_table\n{flow_table}')
            return jsonify(flow_table)
        except Exception as e:
            return jsonify({'message': f'Failed to reset cell {cell_id}  Host {host_id}: {e}'}), 500

#=================================================================================================================
# Route for home page
@app.route('/home', methods=['GET', 'POST'])
@login_required # Login protection
def home():
    if request.method == 'POST':
        cell_id = request.form.get('cell_id')
        if cell_id:
            return redirect(url_for('cell_page', cell=f'cell-{cell_id}', filename='switch.html'))
    
    if 'switches_hosts' not in session:
        session['switches_hosts'] = get_switches_hostsnum()

    switches_hosts = session['switches_hosts']
     # # Sort switches_hosts by dpid
    # switches_hosts_sorted = sorted(switches_hosts, key=lambda x: int(x[0], 16))
    # # cells = [f'cell{i+1}' for i in range(len(switches_hosts_sorted))]
    whitelist = read_whitelist()   #------
    print(whitelist)
    if switches_hosts is None:
        return redirect('/')
    # if switches_hosts is not None:
    else:
        Num_switches = len(switches_hosts)
        create_cell_host_pages(switches_hosts)
        return render_template('home.html', N = Num_switches, whitelist=whitelist)


# Route for current cell page
@app.route('/switch_pages/<cell>/<filename>', methods=['GET', 'POST'])
@login_required
def cell_page(cell, filename):
    switches_hosts = get_switches_hostsnum()
    if switches_hosts is None:
        print('122333')
        return redirect('/home')

    cell_index = int(cell.replace('cell-', '')) - 1
    if cell_index >= len(switches_hosts):
        flash('Invalid cell')
        print('1223344443')
        return redirect('/home')

    num_hosts = switches_hosts[cell_index][1]
    hosts = [f'host-{j+1}' for j in range(num_hosts)]
    
    if request.method == 'POST':
        host_action = request.form.get('host_action')
        host_name = request.form.get('host_name')
        if host_action == 'disconnect':
            return jsonify({'message': f'{host_name} disconnected successfully'})
        elif host_action == 'limit_speed':
            return jsonify({'message': f'{host_name} speed limited successfully'})
        elif host_action == 'view_data':
            return jsonify({'message': f'{host_name} data viewed successfully'})
    
    return render_template(f'switch_pages/{cell}/{filename}', cell=cell, hosts=hosts)


#endregion
# ============================================



# Run the application
if __name__ == "__main__":
    # Start the Flask application
    app.run(debug=True)