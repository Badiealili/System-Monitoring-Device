import pygal
from pygal.style import Style
from pygal import Config
import sqlite3
import time
from datetime import datetime
import os

path = '/home/b4d13/Desktop/coding/ceri/sysAdmin/mini_projet'
con = sqlite3.connect(path + '/data.db')
cursor = con.cursor()
cursor.execute('SELECT Window_Size FROM Config;')
window_size = cursor.fetchone()[0]
# Timestamp to sign the charts filenames (for auto reload in the front)
timestamp = int(time.time())

# Remove old charts
for root, dirs, files in os.walk(path + '/static/charts'):
    for file in files:
        file_path = os.path.join(root, file)
        os.remove(file_path)

# CPU Chart Configuration
style = Style(
    opacity= '.8',
    opacity_hover= '.8',
    colors=('#1393E2','#FF0000'),
    guide_stroke_dasharray='none',
    guide_stroke_color='#A0A0A0',
    major_guide_stroke_dasharray='none',
    major_guide_stroke_color='#A0A0A0',
    stroke_width_hover='1',
    stroke_opacity_hover='1',
)

config = Config()
config.interpolate = 'cubic'
config.show_legend=False
config.fill=True
config.show_dots=False
config.show_x_guides=True
config.x_label_rotation = 20
config.height=500
config.css = (..., '../../chart-config.css')

cpu_line_chart = pygal.Line(style=style, config=config)


cursor.execute(f"SELECT Timestamp, CPU_Usage FROM Sondes ORDER BY Timestamp DESC LIMIT {window_size};")
rows = cursor.fetchall()
time_labels = [rows[_][0] for _ in range(len(rows))][::-1]
values = [rows[_][1] for _ in range(len(rows))][::-1]

cursor.execute("SELECT CPU_Usage FROM config;")
max_value = cursor.fetchone()[0]

cpu_line_chart.x_labels = [datetime.fromtimestamp(ts).strftime("%H:%M") for ts in time_labels]
cpu_line_chart.y_labels = range(0,101,10)
cpu_line_chart.add("Current",values)
cpu_line_chart.add("Max",[max_value]*len(values), fill=False ,stroke_width='4')

cpu_line_chart.render_to_file(path + f'/static/charts/CPU_{timestamp}.svg')

# RAM Chart Configuration

style.colors = ('#DD1464','#FF0000')
ram_line_chart = pygal.Line(style=style, config=config)

cursor.execute(f"SELECT Timestamp, RAM_Usage FROM Sondes ORDER BY Timestamp DESC LIMIT {window_size};")
rows = cursor.fetchall()
time_labels = [rows[_][0] for _ in range(len(rows))][::-1]
values = [rows[_][1] for _ in range(len(rows))][::-1]

cursor.execute("SELECT RAM_Usage FROM config;")
max_value = cursor.fetchone()[0]

ram_line_chart.x_labels = [datetime.fromtimestamp(ts).strftime("%H:%M") for ts in time_labels]
ram_line_chart.y_labels = range(0,101,10)
ram_line_chart.add("Current",values)
ram_line_chart.add("Max",[max_value]*len(values), fill=False ,stroke_width='4')

ram_line_chart.render_to_file(path + f'/static/charts/RAM_{timestamp}.svg')

# Free Disk Space Chart Configuration

style.colors = ('#FA7F03','#FF0000')
disk_line_chart = pygal.Line(style=style, config=config)

cursor.execute(f"SELECT Timestamp, Free_Disk_Space FROM Sondes ORDER BY Timestamp DESC LIMIT {window_size};")
rows = cursor.fetchall()
time_labels = [rows[_][0] for _ in range(len(rows))][::-1]
values = [rows[_][1] for _ in range(len(rows))][::-1]

cursor.execute("SELECT Free_Disk_Space FROM config;")
max_value = cursor.fetchone()[0]

disk_line_chart.x_labels = [datetime.fromtimestamp(ts).strftime("%H:%M") for ts in time_labels]
disk_line_chart.y_labels = range(0,101,10)
disk_line_chart.add("Current",values)
disk_line_chart.add("Max",[max_value]*len(values), fill=False ,stroke_width='4')

disk_line_chart.render_to_file(path + f'/static/charts/Disk_{timestamp}.svg')

# Process Count Chart Configuration

style.colors = ('#16DB93','#FF0000')
process_line_chart = pygal.Line(style=style, config=config)

cursor.execute(f"SELECT Timestamp, Number_Processes FROM Sondes ORDER BY Timestamp DESC LIMIT {window_size};")
rows = cursor.fetchall()
time_labels = [rows[_][0] for _ in range(len(rows))][::-1]
values = [rows[_][1] for _ in range(len(rows))][::-1]

cursor.execute("SELECT Number_Processes FROM config;")
max_value = cursor.fetchone()[0]

process_line_chart.x_labels = [datetime.fromtimestamp(ts).strftime("%H:%M") for ts in time_labels]
process_line_chart.y_labels = range(0,501,50)
process_line_chart.add("Current",values)
process_line_chart.add("Max",[max_value]*len(values), fill=False ,stroke_width='4')

process_line_chart.render_to_file(path + f'/static/charts/Process_{timestamp}.svg')

# Active Users Count Chart Configuration

style.colors = ('#414073','#FF0000')
user_line_chart = pygal.Line(style=style, config=config)

cursor.execute(f"SELECT Timestamp, Number_Active_Users FROM Sondes ORDER BY Timestamp DESC LIMIT {window_size};")
rows = cursor.fetchall()
time_labels = [rows[_][0] for _ in range(len(rows))][::-1]
values = [rows[_][1] for _ in range(len(rows))][::-1]

cursor.execute("SELECT Number_Active_Users FROM config;")
max_value = cursor.fetchone()[0]

user_line_chart.x_labels = [datetime.fromtimestamp(ts).strftime("%H:%M") for ts in time_labels]
user_line_chart.y_labels = range(0,11,1)
user_line_chart.add("Current",values)
user_line_chart.add("Max",[max_value]*len(values), fill=False ,stroke_width='4')

user_line_chart.render_to_file(path + f'/static/charts/Users_{timestamp}.svg')

con.commit()
cursor.close()
con.close()