#! python3

import os
import paho.mqtt.client as mqtt
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

broker_address=os.environ["MQTT_HOST_IP"]
client_name="scan_reader"
topic_name="scan_new_file"

file_path="/data/eingang/Posteingang"

###########################################################
#                    MQTT Client                          #
###########################################################

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

def publish_message(message):
    print("creating new instance")
    client = mqtt.Client(client_name)
    client.on_message=on_message

    print("connecting to broker")
    client.connect(broker_address)
    client.loop_start()

    print("Subscribing to topic",topic_name)
    client.subscribe(topic_name)

    print("Publishing message to topic",topic_name)
    client.publish(topic_name, "New file at " + file_path)

    time.sleep(5)
    client.loop_stop()

###########################################################
#                    File Watcher                         #
###########################################################

patterns = "*"
ignore_patterns = ""
ignore_directories = False
case_sensitive = True
event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

def on_created(event):
    print(f"hey, {event.src_path} has been created!")
    publish_message(f"hey, {event.src_path} has been created!")

def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")
    publish_message(f"what the f**k! Someone deleted {event.src_path}!")

def on_modified(event):
    print(f"hey buddy, {event.src_path} has been modified")
    publish_message(f"hey buddy, {event.src_path} has been modified")

def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")
    publish_message(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")

event_handler.on_created = on_created
event_handler.on_deleted = on_deleted
event_handler.on_modified = on_modified
event_handler.on_moved = on_moved

go_recursively = True
my_observer = Observer()
my_observer.schedule(event_handler, file_path, recursive=go_recursively)

my_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()

my_observer.join()
