from flask import Flask, render_template, jsonify, request, redirect
import sqlite3
import json
import os
import subprocess

path="/home/b4d13/Desktop/coding/ceri/sysAdmin/mini_projet"
db_path = path + '/data.db'

latest_alert = json.loads(open('latest-alert.json', 'r').read())
data = {}

def update_stats():
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    global data
    cursor.execute("SELECT Window_Size FROM Config;")
    window_size = cursor.fetchone()[0]
    data['window_size'] = window_size

    cursor.execute(f"SELECT Timestamp, CPU_Usage FROM Sondes ORDER BY Timestamp DESC LIMIT {window_size};")
    res = cursor.fetchall()
    s = 0
    for line in res:
        s+=line[1]

    data['CPU'] = {
        "avg": float(str(s / len(res))[:4]),
        "min": min([line[1] for line in res]),
        "max": max([line[1] for line in res])
    }

    cursor.execute(f"SELECT Timestamp, RAM_Usage FROM Sondes ORDER BY Timestamp DESC LIMIT {window_size};")
    res = cursor.fetchall()
    s = 0
    for line in res:
        s+=line[1]

    data['RAM'] = {
        "avg": float(str(s / len(res))[:4]),
        "min": min([line[1] for line in res]),
        "max": max([line[1] for line in res])
    }

    cursor.execute(f"SELECT Timestamp, Free_Disk_Space FROM Sondes ORDER BY Timestamp DESC LIMIT {window_size};")
    res = cursor.fetchall()
    s = 0
    for line in res:
        s+=line[1]

    data['Disk'] = {
        "avg": float(str(s / len(res))[:4]),
        "min": min([line[1] for line in res]),
        "max": max([line[1] for line in res])
    }

    cursor.execute(f"SELECT Timestamp, Number_Processes FROM Sondes ORDER BY Timestamp DESC LIMIT {window_size};")
    res = cursor.fetchall()
    s = 0
    for line in res:
        s+=line[1]

    data['Process'] = {
        "avg": float(str(s / len(res))[:4]),
        "min": min([line[1] for line in res]),
        "max": max([line[1] for line in res])
    }

    cursor.execute(f"SELECT Timestamp, Number_Active_Users FROM Sondes ORDER BY Timestamp DESC LIMIT {window_size};")
    res = cursor.fetchall()
    s = 0
    for line in res:
        s+=line[1]

    data['Users'] = {
        "avg": float(str(s / len(res))[:4]),
        "min": min([line[1] for line in res]),
        "max": max([line[1] for line in res])
    }

    con.commit()
    cursor.close()
    con.close()

def update_config_table(data):
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    query = f"""UPDATE Config SET 
                CPU_Usage = {data['max-cpu-usage'][0]},
                RAM_Usage = {data['max-ram-usage'][0]},
                Free_Disk_Space = {data['min-disk-space'][0]},
                Number_Processes = {data['max-processes'][0]},
                Number_Active_Users = {data['max-users'][0]},
                Window_Size = {data['window-size'][0]};
                
    """
    cursor.execute(query)
    con.commit()
    cursor.close()
    con.close()

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_charts')
def get_charts():
    subprocess.run(['python', path + '/data-visualizer.py'])
    return jsonify(os.listdir('static/charts'))

@app.route('/get_stats')
def get_stats():
    update_stats()
    return jsonify(data)

@app.route('/get_latest_alert')
def get_latest_alert():
    return jsonify(open('latest-alert.json').read())

@app.route('/update_config', methods=['POST'])
def update_config():
    data = request.form.to_dict(flat=False)
    update_config_table(data)
    return redirect('/')


if __name__=='__main__':
    app.run(debug=True)