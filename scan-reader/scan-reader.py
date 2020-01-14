#! python3

import json
import os
import paho.mqtt.client as mqtt
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

broker_address=os.environ["MQTT_HOST_IP"]
client_name="scan_reader"

scan_reader_topic_name="scan_new_file"
file_path="/data/eingang/Posteingang"


###########################################################
#                    MQTT Client                          #
###########################################################

class ScannerMqttClient:

    def __init__(self, client_name):
        self.client = mqtt.Client(client_name)
        self.known_topics = []

    def connect(self, broker_address):
        print(f"Connecting to mqtt broker @ {broker_address}")
        self.client.connect(broker_address)
        self.client.loop_start()

    def disconnect(self, ):
        print("Disconnecting from the mqtt broker")
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic, message):
        print(f"Publishing a message @ the topic '{topic}' with the content: {message}")
        self.client.publish(topic, message)

    def subsribe(self, topic):
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
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
    def __enter__(self):
        print("Setting up the file watcher variables...")
        self.patterns = [ "*.tif", "*.jpg" ]
        self.ignore_patterns = ""
        self.ignore_directories = False
        self.case_sensitive = True

        self.event_handler = PatternMatchingEventHandler(
            self.patterns,
            self.ignore_patterns,
            self.ignore_directories,
            self.case_sensitive
        )

        self.event_handler.on_created = self.on_created
        #self.event_handler.on_modified = self.on_modified

        self.observer = Observer()

    def __exit__(self, exc_type, exc_value, traceback):
        print("Stopping the observer...")
        self.observer.stop()
        self.observer.join()

    def on_created(self, event):
        self.schedule_file(event.src_path)

    #def on_modified(self, event):
       # print(f"hey buddy, {event.src_path} has been modified")
        # publish_message(f"hey buddy, {event.src_path} has been modified")

    def watch_directory(self, directory):
        print("Setting up an observer on ", directory, " with ", self.observer)
        print("Event handler is ", self.event_handler)
        self.observer.schedule(self.event_handler, directory, recursive=True)
        self.observer.start()

    def schedule_file(self, file_path):
        print("Scheduling file ", file_path)
        tagged_file_path = self.add_file_tag(file_path, "scheduled")
        self.mqtt_client.publish(scan_reader_topic_name, json.dumps({ 'file_path': tagged_file_path }))

    def add_file_tag(self, file_path, tag_name):
        base_file_path, extension = os.path.splitext(file_path)
        tagged_file_path = base_file_path + "." + tag_name + extension
        shutil.copy2(file_path, tagged_file_path)
        return tagged_file_path


if __name__ == "__main__":
    mqtt_client = ScannerMqttClient(client_name)
    mqtt_client.connect(broker_address)
    scan_reader_file_watcher = ScanReaderFileWatcher(mqtt_client)

    with scan_reader_file_watcher:
        scan_reader_file_watcher.watch_directory(file_path)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            my_observer.stop()

        my_observer.join()
