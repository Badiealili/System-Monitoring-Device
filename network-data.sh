#!/bin/bash
public_ip=$(curl -s ifconfig.me)
mac_address=$(ifconfig wlan0 | grep -o -E '([0-9a-fA-F]{2}:){5}([0-9a-fA-F]{2})')
table_name="Sondes"

DB_FILE="/home/b4d13/Desktop/coding/ceri/sysAdmin/mini_projet/data.db"
QUERY="UPDATE \"$table_name\" SET Public_IP_Address = \"$public_ip\", MAC_Address = \"$mac_address\" WHERE Timestamp = (SELECT MAX(Timestamp) FROM \"$table_name\");"

sqlite3 "$DB_FILE" "$QUERY"