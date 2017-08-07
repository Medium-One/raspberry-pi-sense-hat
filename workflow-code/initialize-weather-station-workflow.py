'''
Raspberry Pi Weather Station Initialization
Created: June 28, 2017
By: Dan Kane
 
This workflow is triggered when the Raspberry Pi client successfully connects to the Medium One
cloud via MQTT. As soon as this happens, the Medium One MQTT broker publishes an "Init_Request" which
initializes the RPi LED matrix and starts the Sense Hat pressure sensor so it is ready for use.
 
'''
 
import MQTT
import Store
 
Store.set_global_data("initialized", "False") # This will remain false in later workflows until the client
                                              # publishes an 'Initialized' : 'True' message.  It will be used to
                                              # make sure scheduled data requests don't begin until the RPi is
                                              # ready.
'''
The following are not used by this simple demonstration, however, they could be used to
store weather data for transmission via email or for more detailed custom analysis.
 
Store.set_global_data("Temperature_Data", "") # Initialize Temperature_Data as empty Store variable
Store.set_global_data("Pressure_Data", "") # Initialize Pressure_Data as empty Store variable
Store.set_global_data("Humidity_Data", "") # Initialize Humidity_Data as empty Store variable
 
'''
 
MQTT.publish_event_to_client('Rasp_Pi','{"Init_Request":"True"}',encoding='utf-8')
