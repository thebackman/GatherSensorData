""" gather indoor air data, run every 5 minutes with cron """

# -- cron

# */5 * * * * python3 /home/pi/Projects/GatherSensorData/temp_and_friends.py

# -- libs

import confs
from datetime import datetime
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_air_quality import BrickletAirQuality
import sqlite3

# -- run

if __name__ == "__main__":
    
    # Create IP connection
    ipcon = IPConnection() 

    # setup air quality bricklet
    air = BrickletAirQuality(confs.AIR_UID, ipcon)

    # connect
    ipcon.connect(confs.HOST, confs.PORT)
    
    # get all the values that the sensor has to offer and unpack
    iaq_index, iaq_index_accuracy, temperature, humidity, air_pressure = air.get_all_values()
    
    # save it in the data base
    
    now = datetime.now()
    conn = sqlite3.connect(confs.AIR_DB)
    cur = conn.cursor()    
    cur.execute("""
                INSERT INTO air_measures_10min
                (time, temp, humidity, pressure, IAQ, IAQ_accuracy)
                VALUES (?,?,?,?,?,?);
                """,
                (now,
                 temperature / 100.0,
                 humidity / 100.0,
                 air_pressure / 100.0,
                 iaq_index,
                 iaq_index_accuracy))
    
    # commit changes and close
    conn.commit()
    conn.close()
    
    # when done disconnect
    ipcon.disconnect()
