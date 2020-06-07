""" setup data storage """

# -- libs

import sqlite3
import confs

# --create database for decibel data

sound_conn = sqlite3.connect(confs.SOUND_DB)
cur = sound_conn.cursor()

# table def for the minute data. This will hold one measurement per minute
# of the sound level in decibel dB(A). Each entry will be the aggregation
# of one measurement per second.

decibel = """
CREATE TABLE 'decibel_minute_data' (
'key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
'time' TEXT,
'db_min' NUMERIC,
'db_mean' NUMERIC,
'db_max' NUMERIC)
"""

cur.execute(decibel)
sound_conn.commit()
sound_conn.close()

