""" collects decibel data on second level

Idea is to get a 'profile' of the ambient sound level

The script will, when run continiously will generate

60 * 24 * 365 = 525600 data rows per year

"""

# -- cron

# @reboot python3 /home/pi/Projects/GatherSensorData/sound.py

# TODO:

# see if there is smarter way to add multiple numpy aggregations

# -- libs

import numpy as np
import confs
from datetime import datetime
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_sound_pressure_level import BrickletSoundPressureLevel
import logging
import sqlite3
import os

# -- logging

logging.basicConfig(
        level=logging.DEBUG,
        format = confs.FORMAT,
        handlers=[
        logging.FileHandler(confs.LOGFILE),
        logging.StreamHandler()])

# -- globals

HOST = "localhost"
PORT = 4223
UID = "NZ2"
CURRENT_TIME = datetime.now()
PID = os.getpid()

# -- holders

one_minute_list = []

# -- functions

def callis(param):
    """ callback function """
    
    # what is the time each time the callback is "called"?
    t0 = datetime.now().strftime("%H:%M:%S:%f")
    print(f"time is {t0}")
    
    # get the decibel value
    val = spl.get_decibel() / 10
    print(f"decibel value is {val}")
    
    # append the value to the list
    one_minute_list.append(val)
    
    # check the length of the list
    list_len = len(one_minute_list)
    print(f"length of one_minute_list is {list_len}")
    
    # when we have 60 measurements, flush it
    if len(one_minute_list) == 60:
        print("flushing 10 seconds of data")
        collect_and_flush_one_minute(one_minute_list)


def collect_and_flush_one_minute(one_minute_list):
    """ collect the list and flush the contents """
    
    # create a numpy array and append to the ten min list
    num = np.array(one_minute_list)
    
    test_len = len(num)
    print(f"the length of the numpy array is {test_len}")
    
    # send it to be saved
    aggregate_and_save(num)
    
    print(">>> Next minute")
    
    del one_minute_list[:]


def aggregate_and_save(np_arr):
    
    # construct variables
    the_mean = np.mean(np_arr)
    the_median = np.median(np_arr)
    the_min = np.min(np_arr)
    the_max = np.max(np_arr)
    
    now = datetime.now()
    
    # write into the db
    conn = sqlite3.connect(confs.SOUND_DB)
    cur = conn.cursor()    
    cur.execute("""
                INSERT INTO decibel_minute_data
                (time, db_min, db_mean, db_median, db_max)
                VALUES (?,?,?,?,?);
                """,
                (now,
                 the_min,
                 the_mean,
                 the_median,
                 the_max))
    
    # commit changes and close
    conn.commit()
    conn.close()

def save_pid(pid):
    
    now = datetime.now()
    
    # write into the db
    conn = sqlite3.connect(confs.SOUND_DB)
    cur = conn.cursor()    
    cur.execute("""
                INSERT INTO last_pid
                (time, pid)
                VALUES (?,?);
                """,
                (now,
                 pid))
    
    # commit changes and close
    conn.commit()
    conn.close()
    

if __name__ == "__main__":

    # -- run
    
    # create a log entry
    logging.info(f"time is {CURRENT_TIME} and script is executed after restart")
    logging.info(f"start gathering decibel measures")
    logging.info(f"PID is {PID}")
    logging.info("------------------------------------------------------------")
    
    # write pid to db
    save_pid(PID)
    
    # -- below is more or less taken directly from tinkeforge docs

    # Create IP connection
    ipcon = IPConnection() 
    
    # Create device object
    spl = BrickletSoundPressureLevel(UID, ipcon)

    # Connect to brickd, dont use the device before ipcon is connected
    ipcon.connect(HOST, PORT) 

    # Register decibel callback to function cb_decibel
    spl.register_callback(spl.CALLBACK_DECIBEL, callis)

    # Set period for decibel callback to 1s (1000ms) without a threshold
    spl.set_decibel_callback_configuration(1000, False, "x", 0, 0)

    # input("Press key to exit\n") # to break out
    ipcon.disconnect()

