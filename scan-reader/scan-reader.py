#! python3

import json
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

class ScannerMqttClient:

    def __init__(self, client_name):
        self.client = mqtt.Client(client_name)
        self.known_topics = []

    def connect(broker_address):
        print(f"Connecting to mqtt broker @ {broker_address}")
        self.client.connect(broker_address)
        self.client.loop_start()

    def disconnect():
        print("Disconnecting from the mqtt broker")
        self.client.loop_stop()
        self.client.disconnect()

    def publish(topic, message):
        print(f"Publishing a message @ the topic '{topic}' with the content: {message}")
        client.publish(topic, message)

    def subsribe(topic):
        if not topic in self.known_topics:
            print(f"Adding a new subscribtion to the topic '{topic}'")
            self.known_topics.append(topic)
            self.client.subscribe(topic)
        else:
            print(f"Already subsribed to the topic '{topic}'")



###########################################################
#                    File Watcher                         #
###########################################################

class ScanReaderFileWatcher:
    def __enter__(self):
        self.patterns = "*"
        self.ignore_patterns = ""
        self.ignore_directories = False
        self.case_sensitive = True
        self.event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

        self.event_handler.on_created = self.on_created
        self.event_handler.on_deleted = self.on_deleted
        self.event_handler.on_modified = self.on_modified
        self.event_handler.on_moved = self.on_moved

        self.observer = Observer()

    def __exit__(self, exc_type, exc_value, traceback):
        self.observer.stop()
        self.observer.join()

    def on_created(event):
        print(f"hey, {event.src_path} has been created!")
        publish_message(json.dumps({ file_path: event.src_path }))

    def on_deleted(event):
        print(f"what the f**k! Someone deleted {event.src_path}!")
        # publish_message(f"what the f**k! Someone deleted {event.src_path}!")

    def on_modified(event):
        print(f"hey buddy, {event.src_path} has been modified")
        # publish_message(f"hey buddy, {event.src_path} has been modified")

    def on_moved(event):
        print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")
        # publish_message(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")

    def watch_directory(self, directory):
        self.observer.schedule(self.event_handler, directory, recursive=True)
        self.observer.start()


# TODO Add mqtt client as argument to file watcher
with ScanReaderFileWatcher() as file_watcher:
    file_watcher.watch(file_path)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()

my_observer.join()
