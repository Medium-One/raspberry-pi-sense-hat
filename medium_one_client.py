# Preliminary RPi MQTT Client
# Written by Dan Kane
# June 20, 2017
 
 
# V 02 Updated July 13, 2017
 
# In the previous version, a dropped MQTT connection did not resubscribe to
# Medium One topic.  V02 corrects that problem by moving the publish 'Connected:True'
# and subscribe to Medium One topic into the on_connect callback function
 
# Adds byte conversion to string for all incoming payloads.  This eliminates the
# b (for bytes) in front of the printed payload data for debugging
 
# Added proper JSON decoding in the on_message callback method so that the if-else
# clause works with the actual dictionary keys
 
import paho.mqtt.client as mqtt
import ssl
import time
import json
from sense_hat import SenseHat
 
# Definitions for sense hat led display.  See http://pythonhosted.org/sense-hat/api/
# for instructions on how to use the set_pixels function
 
d = [0,0,0] # dark.  The 3 list components are R, G, B values
w = [100,100,100] # white.
b = [0,0,150] # blue.
 
# The 64 elements below specify the color to display on each LED in the 8x8 matrix
logo = [
b, b, b, b, b, b, b, b,
b, w, d, d, d, d, w, b,
b, w, w, d, d, w, w, b,
b, w, d, w, w, d, w, b,
b, w, d, d, d, d, w, b,
b, w, d, d, d, d, w, b,
b, w, d, d, d, d, w, b,
b, b, b, b, b, b, b, b
]
 
# Create a SenseHat object to access all sense hat features
# The sensehat package must be installed on the pi first by following
# instructions here: http://pythonhosted.org/sense-hat/
sense = SenseHat()
 
# Medium One Credentials from Medium One Sandbox
# These all need to be set to values obtained when registering with Medium One
m1_user = "device"
m1_password = "Abxxx3$!"
m1_apikey = "RVWEY2BLKAXJL6UEPEONQFZQGVRXXXXXXVQTGZBQGQ3TAMBQ"
m1_project_id = "0KwhxxxUBdQ" #Project MQTT ID
m1_userMQTT_id = "yazNxxxUyH8" #User MQTT ID
m1_client_id = "Rasp_Pi" #Can be anything.  Needs to match publish requests from Medium One cloud
 
data_connected = {"event_data":{"Connected":"True"}} # Payload to transmit when connected
m1_payload = json.dumps(data_connected) # Medium One MQTT accepts JSON format
 
MQTT_username = m1_project_id + "/" + m1_userMQTT_id  # Medium One specification for user credential
MQTT_password = m1_apikey + "/" + m1_password # Medium One specification for password credential
 
m1_topic_publish = "0/"+m1_project_id+"/"+m1_userMQTT_id+"/"+m1_client_id
m1_topic_subscribe = "1/"+m1_project_id+"/"+m1_userMQTT_id+"/"+m1_client_id+"/event"
 
def process_temp_request(msg):
    temperature = sense.get_temperature()
    print("Topic: "+str(msg.topic)) #For debugging
    print("QOS: "+str(msg.qos)) #For debugging
    print("Payload: "+ msg.payload.decode("utf-8", "strict")) #For debugging
    temp_data = {"event_data":{"Temperature" : str(temperature)}}
    m1_temp_payload = json.dumps(temp_data)
    m1_client.publish(topic=m1_topic_publish, payload=m1_temp_payload, qos=0, retain=False)
 
def process_pressure_request(msg):
    pressure = sense.get_pressure()
    print("Topic: "+str(msg.topic)) #For debugging
    print("QOS: "+str(msg.qos)) #For debugging
    print("Payload: "+ msg.payload.decode("utf-8", "strict")) #For debugging
    pressure_data = {"event_data":{"Pressure" : str(pressure)}}
    m1_pressure_payload = json.dumps(pressure_data)
    m1_client.publish(topic=m1_topic_publish, payload=m1_pressure_payload, qos=0, retain=False)
 
def process_humidity_request(msg):
    humidity = sense.get_humidity()
    print("Topic: "+str(msg.topic)) #For debugging
    print("QOS: "+str(msg.qos)) #For debugging
    print("Payload: "+ msg.payload.decode("utf-8", "strict")) #For debugging
    humidity_data = {"event_data":{"Humidity" : str(humidity)}}
    m1_humidity_payload = json.dumps(humidity_data)
    m1_client.publish(topic=m1_topic_publish, payload=m1_humidity_payload, qos=0, retain=False)
 
def process_init_request(msg):
    #dummy read of pressure to give the pressure sensor time to initialize.  After the first
    #read, there is a short warm up period when it returns zero.
    dummy = sense.get_pressure()
    print("Topic: "+str(msg.topic)) #For debugging
    print("QOS: "+str(msg.qos)) #For debugging
    print("Payload: "+ msg.payload.decode("utf-8", "strict")) #For debugging
    sense.set_pixels(logo)
    init_data = {"event_data":{"Initialized" : "True"}}
    m1_init_payload = json.dumps(init_data)
    m1_client.publish(topic=m1_topic_publish, payload=m1_init_payload, qos=0, retain=False)
 
def process_set_pixels(msg):
    pass # TBD tag = Pixels_Request, data = list of 64 RGB values to specify display
         # uses sense.set_pixels
 
def process_show_message(msg):
    pass # TBD tag = Message_Request. data = text string, scroll speed, text colour, back colour
         # uses sense.show_message
   
def on_connect(m1_client, obj, flags, rc):
    print("rc: "+str(rc))
 
    # Publish "Connected:True" event to Medium One broker
    m1_client.publish(topic=m1_topic_publish, payload=m1_payload, qos=0, retain=False)
 
    # Subscribe to Medium One topic in order to receive requests for information
    # from Raspberry Pi.
    m1_client.subscribe(topic = m1_topic_subscribe, qos=0)
 
def on_message(m1_client, obj, msg):
    payload_string = msg.payload.decode("utf-8", "strict") # Convert from bytes to str
    payload_dict = json.JSONDecoder().decode(payload_string) # Create a Python dict object from the string
    if ("Init_Request" in payload_dict):
        process_init_request(msg)
    elif ("Temp_Request" in payload_dict):
        process_temp_request(msg)
    elif ("Pressure_Request" in payload_dict):
        process_pressure_request(msg)
    elif ("Humidity_Request" in payload_dict):
        process_humidity_request(msg)
    else:
        print("Unexpected MQTT Request: "+payload_string)
 
def on_publish(m1_client, obj, mid):
    print("mid: "+str(mid))
 
def on_subscribe(m1_client, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))
    print("Subscription Result: "+str(obj))
 
def on_log(m1_client, obj, level, string):
    print(string)
 
m1_client = mqtt.Client(client_id=m1_client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
 
m1_client.on_message = on_message
m1_client.on_connect = on_connect
m1_client.on_publish = on_publish
m1_client.on_subscribe = on_subscribe
m1_client.on_log = on_log
 
m1_client.username_pw_set(username=MQTT_username, password=MQTT_password)
m1_client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
 
# Certificates aren't currently used, but this is how you might point to them in the future.
# m1_client.tls_set(ca_certs="/etc/ca-certificates/ca-certs.pem", tls_version=ssl.PROTOCOL_TLSv1_2)
 
# Establish connection with Medium One broker
m1_client.connect(host="mqtt.mediumone.com", port=61620, keepalive=300)
 
# The mi_client.loop_start() call creates a new thread which handles MQTT communication
# It keeps the connection alive until loop_stop() is called.
#m1_client.loop_start()
m1_client.loop_forever()
 
# The separate thread created with the m1_client.loop_start() call now runs
# in the background handling all MQTT traffic.  Incoming requests are handled
# by the 'on_message' function.  'on_connect' handles the initial connection
# as well as the case where the Pi must reconnect due to a network problem
