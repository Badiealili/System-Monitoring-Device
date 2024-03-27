import sqlite3

table_name = "Config"
con = sqlite3.connect("/home/b4d13/Desktop/coding/ceri/sysAdmin/mini_projet/data.db")
cursor = con.cursor()

def create_table():
    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
    CPU_Usage REAL,
    RAM_Usage REAL,
    Free_Disk_Space REAL,
    Number_Processes INTEGER,
    Number_Active_Users INTEGER,
    History_Limit INTEGER,
    Window_Size INTEGER
    );
"""
    cursor.execute(query)

def insert_params(cpu_usage, ram_usage, free_disk_space, number_processes, number_active_users, history_limit, window_size):
    query = f"""
    INSERT INTO {table_name} 
    (CPU_Usage, RAM_Usage, Free_Disk_Space, Number_Processes, Number_Active_Users, History_Limit, Window_Size)
    VALUES ({cpu_usage}, {ram_usage}, {free_disk_space}, {number_processes}, {number_active_users}, {history_limit}, {window_size}) 
""" 
    cursor.execute(query)

cpu_usage = input("Max CPU Usage>> ")
ram_usage = input("Max RAM Usage>> ")
free_disk_space = input("Min Disk Space>> ")
number_processes = input("Max Number of Processes>> ")
number_active_users = input("Max Number of Active Users>> ")
history_limit = input("History Limit>> ")
window_size = input("Window Size>> ")

create_table()
insert_params(cpu_usage, ram_usage, free_disk_space, number_processes, number_active_users, history_limit, window_size)

con.commit()
cursor.close()
con.close()