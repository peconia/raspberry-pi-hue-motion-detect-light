from phue import Bridge
import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta
import config

GPIO.setmode(GPIO.BCM)

detection_pin = 17
GPIO.setup(detection_pin, GPIO.IN)

b = Bridge(config.bridge_ip)  # ip of the hue bridge
b.connect()


class MotionSensorLight:

    def __init__(self):
        self.last_turned_on = datetime.now()
        self.light_on = False
        GPIO.add_event_detect(detection_pin, GPIO.RISING, callback=self.on_motion_detected)

    def turn_on(self):
        b.set_light(config.light_name, 'on', True, transitiontime=10)
        self.light_on = True
        self.last_turned_on = datetime.now()

    def turn_off(self):
        b.set_light(config.light_name, 'on', False)
        self.light_on = False

    def on_motion_detected(self, detection_pin):
        self.last_turned_on = datetime.now()
        if not self.light_on:
            self.turn_on()

try:
    light = MotionSensorLight()
    while True:
        if light.light_on and light.last_turned_on + timedelta(minutes=3) < datetime.now():
            light.turn_off()
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()

