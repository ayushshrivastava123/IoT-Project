import RPi.GPIO as GPIO
from gpiozero import Buzzer
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
from datetime import date, datetime

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  
GPIO.setup(17,GPIO.IN)   
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
myMQTTClient.publish("voice", "connected", 0)
#loop and publish sensor reading
while 1:
   now = datetime.utcnow()
   now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
   payload = '{ "timestamp": "' + now_str + '","Voice": ' + "{:.2f}".format(GPIO.input(17)) + ' }'
   print payload
   myMQTTClient.publish("voice", payload, 0)
   time.sleep(.01)

