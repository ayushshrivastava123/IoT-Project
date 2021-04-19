import RPi.GPIO as GPIO
import Adafruit_DHT as dht
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
 
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
 
# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("123afhlss411")
myMQTTClient.configureEndpoint("*************.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/awsiot/VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem", "/home/pi/awsiot/f948372088-private.pem.key", "/home/pi/awsiot/f948372088-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
 
#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("homepi/dht22", "connected", 0)
 
#loop and publish sensor reading
while 1:
    now = datetime.utcnow()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') 
    h,t = dht.read_retry(dht.DHT22, 4)
    print 'Temp = %.1f"C, Humidity = %.1f%%RH' % (t, h)
    payload = '{ "timestamp": "' + now_str + '","temperature": ' + "{:.2f}".format(t)+ ',"humidity": '+ "{:.2f}".format(h) + ' }'
    print payload
    myMQTTClient.publish("homepi/dht22", payload, 0)
    sleep(10)