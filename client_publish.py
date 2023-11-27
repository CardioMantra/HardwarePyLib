import paho.mqtt.publish as publish

# MQTT broker configuration
broker_address = "192.168.1.12"  # Replace with the address of your MQTT broker
port = 1883  # Replace with the port of your MQTT broker

# Topic to which the message will be published
topic = "test/topic"

# Message to be published
message = "Hello, MQTT!"

# Publish the message
publish.single(topic, message, hostname=broker_address, port=port)
