""" this files holds globals and constants """

# -- libs

import os

# -- paths

PROJ_FOLDER = "/home/pi/Projects/GatherSensorData"
SOUND_DB = os.path.join(PROJ_FOLDER, "sound.db")
LOGFILE = os.path.join(PROJ_FOLDER, "soundlog.log")

# -- logformat

FORMAT = '%(asctime)s %(levelname)s: %(module)s: %(funcName)s(): %(message)s'


