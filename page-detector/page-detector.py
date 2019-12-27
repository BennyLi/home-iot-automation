#! python3

import os
import paho.mqtt.client as mqtt
import time

broker_address=os.environ["MQTT_HOST_IP"]
client_name="page_detector"
input_topic_name="scan_new_file"
output_topic_name="scan_new_prepared_file"


###########################################################
#                    MQTT Client                          #
###########################################################

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

def publish_message(message):
    print(f"Connecting to output topic {output_topic_name}")
    client = mqtt.Client(client_name)
    client.connect(broker_address)
    client.loop_start()
    client.subscribe(topic_name)
    print("Publishing message to topic", output_topic_name)
    client.publish(topic_name, message)

    time.sleep(5)
    client.loop_stop()



if __name__ == "__main__":
    print("Wait a moment for mqtt to initialise...")
    time.sleep(5)
    print(f"Connecting to input topic {input_topic_name}")
    client = mqtt.Client(client_name)
    client.on_message=on_message
    client.connect(broker_address)
    client.loop_start()
    client.subscribe(input_topic_name)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client.loop_stop()

