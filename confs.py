""" this files holds globals and constants """

# -- libs

import os

# -- paths

PROJ_FOLDER = "/home/pi/Projects/GatherSensorData"
SOUND_DB = os.path.join(PROJ_FOLDER, "sound.db")
LOGFILE = os.path.join(PROJ_FOLDER, "soundlog.log")
AIR_DB = os.path.join(PROJ_FOLDER, "air.db")

# -- logformat

FORMAT = '%(asctime)s %(levelname)s: %(module)s: %(funcName)s(): %(message)s'

# -- connection attributes

HOST = "localhost"
PORT = 4223

MASTER_UID = "6Kvmoe"
SOUND_UID = "NZ2"
AIR_UID = "LfT"
BUTTON_UID = "QnU"