from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_flows', methods=['POST'])
def get_flows():
    base = request.form['base']
    if base != 'undefined':
        print(f'base:{base}')
        base = f'/{base}'
    else: 
        base = ''
    response = requests.get('http://127.0.0.1:8080/flow/switches'+base)
    return jsonify(response.json())  

if __name__ == '__main__':
    app.run(debug=True)
