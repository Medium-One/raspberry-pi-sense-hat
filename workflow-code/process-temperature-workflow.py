# Raspberry Pi Weather Station Temperature Processing
# Created: July 27, 2017
# By: Dan Kane
 
# This workflow demonstrates how to create a processed stream which can be visualized
# on the dashboard or used to trigger other workflows.  The Raspberry Pi reports temperature
# in Celsius.  This workflow converts Celsius to Fahrenheit and creates a processed output
# stream in Fahrenheit.
 
 
TinC = float(IONode.get_input('in1')['event_data']['value'])
TinF = round(TinC*1.8 + 32,2)
 
output_dict = {}
output_dict['Temp_Proc'] = TinF
IONode.set_output('out1', output_dict)
