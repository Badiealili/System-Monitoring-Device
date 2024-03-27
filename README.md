# System Monitoring Program
This project is a minimal system monitor that does the following tasks:
+ Watch for changes in CPU usage, RAM usage, Available disk space, Number of running processes, and number of active users.
+ Display the collected data in a beautiful web interface using line graphs.
+ Send an alert to your email address when a certain limit is exceeded by the system (the limits are fully confirugable via the website)
+ Backup the data in the database every week
+ Restores the latest CERT alert and display it every day

## Usage 
1. Run the following comand via your terminal
`git clone github.com/badiealili/system-monitoring-program`
2. Update the files `backup.py` and `system-data.py` with your email parameters
3. Add your email password to the file `/etc/environment` as an env variable `PASSWORD`
4. Update the path variable everywhere with the correct path to you dir
5. Add the following lines to yor crontab
```bash
* *   * * * your_user_name /path/to/project/dir/data-collection.sh
0 8   * * 1 /bin/python your_user_name /path/to/project/dir/backup.py
0 8   * * * /bin/python your_user_name /path/to/project/dir/html-parser.py
```
6. Launch the server using `python server.py`
7. Configure the settings in the website
8. And we're done! your can watch your system being monitored