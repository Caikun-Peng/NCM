import os
import subprocess
import json

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def merge_and_remove_duplicates(list1, list2):
    combined_list = list1 + list2
    unique_items = {}
    for item in combined_list:
        key = frozenset(item.items())
        if key not in unique_items:
            unique_items[key] = item
    return list(unique_items.values())

def get_white_list():
    json1_path = 'whitelist_default.json'
    json2_path = 'whitelist_to_add.json'
    
    json1_data = load_json(json1_path)
    json2_data = load_json(json2_path)
    
    result_data = merge_and_remove_duplicates(json1_data, json2_data)
    
    save_json(result_data, 'whitelist.json')

class ncm():
    def __init__(self):
        self.mininet_process = None

    def start(self):
        get_white_list()
        self.mininet_process = subprocess.Popen(['xterm', '-hold', '-e', 'mn -c \n python3 net.py'])

    def stop(self):
        close_mininet()

    def restart(self):
        self.stop()
        self.start()

def get_windows():
    try:
        result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')
        return lines
    except subprocess.CalledProcessError:
        return []

def close_window(window_id):
    subprocess.run(['xkill', '-id', window_id])

def close_mininet():
    windows = get_windows()

    print("All windows:")
    for window in windows:
        print(window)

    for window in windows:
        if "mn -c" in window:
            window_id = window.split()[0]
            close_window(window_id)


if __name__ == '__main__':
    net = ncm()
    ryu_process = subprocess.Popen(['xterm', '-e', 'ryu-manager ncm_api.py'])
    net.start()