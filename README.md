# Motion detect light

This is a script to use a motion detector connected to a Raspberry Pi to control the Phillips Hue light in my kitchen. The light is turned on when motion is detected and is automatically turned off after a while if there is no further motion detected.

The hue bridge ip and name for the light must be set in the config file. 

I'm using a slightly modified version of Phue - https://github.com/studioimaginaire/phue/. 
The setup file .python_hue should be placed in /home/pi/ - this has the Bridge details.

I used https://thepihut.com/products/pir-motion-sensor-module connected to pin 17 (BCM).

