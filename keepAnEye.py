# Mahtab Syed — 13 Sep 2015 - http://www.linkedin.com/in/mahtabsyed 
# With thanks to the inspiration - https://www.raspberrypi.org/learning/parent-detector/
import RPi.GPIO as GPIO
import time
import picamera
import datetime
import emailLib

def get_time_stamp():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

def get_file_name():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.jpg")

sensor = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

previous_state = False
current_state = False

cam = picamera.PiCamera()

while True:
    time.sleep(0.1)

    ts = get_time_stamp()

    previous_state = current_state
    current_state = GPIO.input(sensor)
    
    if current_state != previous_state:
        new_state = "HIGH" if current_state else "LOW"
        print("GPIO pin %s is %s at time : %s" % (sensor, new_state, ts))

        if current_state:
            fileName = get_file_name()
            try:
                 # Take a photo and send via email
                cam.vflip = True
                cam.start_preview()
                # Reduce the resolution of camera to make smaller files
                cam.resolution = (320, 240)
                cam.capture(fileName)
                print("Captured photo ", fileName)
            except Exception as e:
                print("Exception...", e)
        else:
           cam.stop_preview()
           emailLib.sendEmail(fileName)