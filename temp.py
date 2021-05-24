from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
from rpi_ws281x import *
import argparse

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def colorWipe(strip, color):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()


# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("project_client")
myMQTTClient.configureEndpoint("a3i8q8ljdrqz7m-ats.iot.us-west-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/Desktop/CmpE181/connect_device_package/AmazonRootCA1.pem", "/home/pi/Desktop/CmpE181/connect_device_package/20a07069bd-private.pem.key", "/home/pi/Desktop/CmpE181/connect_device_package/20a07069bd-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("temp", "connected", 0)
#Custome Callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    if (message.payload == "Cool Temperature"):
        colorWipe(strip, Color(0, 0, 255))  # Green wipe
    elif(message.payload == "Normal Temperature"):
        colorWipe(strip, Color(0, 255, 0))  # Blue wipe
    else:
        colorWipe(strip, Color(255, 0, 0))  # Red wipe
#loop and publish sensor reading
while 1:
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    now = datetime.utcnow()
    print(now)
    date = now.strftime("%x") #e.g. 2016-04-18T06:12:25.877Z
    time = now.strftime("%X")
    file = open("/sys/class/thermal/thermal_zone0/temp")
    temp = float(file.read())/1000
    payload = '{ "Date": "' + date + '","Time": "' + time + '","Temperature": ' + "{:.4f}".format(temp) + '}'
    print (payload)
    myMQTTClient.publish("temp", payload, 0)
    myMQTTClient.subscribe("coolingTemp", 1, customCallback)
    myMQTTClient.subscribe("normalTemp", 1, customCallback)
    myMQTTClient.subscribe("highTemp", 1, customCallback)
 
    sleep(12)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   