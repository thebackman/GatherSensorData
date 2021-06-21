""" turn off the leds on the sensors / bricks on restart - run as cron """

import time
import confs

from tinkerforge.ip_connection import IPConnection

from tinkerforge.brick_master import BrickMaster
from tinkerforge.bricklet_sound_pressure_level import BrickletSoundPressureLevel
from tinkerforge.bricklet_air_quality import BrickletAirQuality
from tinkerforge.bricklet_dual_button_v2 import BrickletDualButtonV2

# Create IP connection
ipcon = IPConnection() 

# bricks and bricklets
master = BrickMaster(confs.MASTER_UID, ipcon)
spl = BrickletSoundPressureLevel(confs.SOUND_UID, ipcon)
air = BrickletAirQuality(confs.AIR_UID, ipcon)
button = BrickletDualButtonV2(confs.BUTTON_UID, ipcon)

# connect
ipcon.connect(confs.HOST, confs.PORT)

# turn on the leds

master.enable_status_led()
spl.set_status_led_config(1)
air.set_status_led_config(1)
button.set_status_led_config(1)

# sleepa while
time.sleep(10)

# turn them off or use auto toggle
master.disable_status_led()
spl.set_status_led_config(0)
air.set_status_led_config(0)
button.set_status_led_config(0)
button.set_led_state(1)

# when done dsiconnect
ipcon.disconnect()
