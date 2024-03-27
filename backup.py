import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime
import time
import sqlite3



path = '/home/b4d13/Desktop/coding/ceri/sysAdmin/mini_projet'
file_path = path + '/data.db'

con = sqlite3.connect(file_path)
cursor = con.cursor()

ts = int(time.time())
date = datetime.fromtimestamp(ts).strftime("%d-%m")

print(date)

# Email details
sender_email = "alili31badie@gmail.com"
receiver_email = "alili31badie@gmail.com"
password = os.getenv("PASSWORD")

# Create message container
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = f"[ARCHIVE]: Database Backup From {date}"

# Attach file
filename = "data.db"  # Change this to your file name
attachment = open(filename, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
msg.attach(part)

# Connect to SMTP server and send email
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, password)
text = msg.as_string()
server.sendmail(sender_email, receiver_email, text)
server.quit()

cursor.execute('DELETE FROM Sondes;')

con.commit()
cursor.close()
con.close()