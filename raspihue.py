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
        # print("motion detected")

        if self.light_on:
            # print("light already on")
            self.last_turned_on = datetime.now()
        else:  # light is off
            time.sleep(0.75)
            if GPIO.input(detection_pin):
                self.last_turned_on = datetime.now()
                self.turn_on()
            else:
                # print("pin not high, not turning light on")
                pass

try:
    light = MotionSensorLight()
    while True:
        if light.light_on and light.last_turned_on + timedelta(minutes=3) < datetime.now():
            light.turn_off()
        time.sleep(0.25)

except KeyboardInterrupt:
    GPIO.cleanup()

