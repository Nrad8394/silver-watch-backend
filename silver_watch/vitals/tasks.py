import time
import paho.mqtt.client as mqtt
from celery import shared_task
from django.conf import settings

MQTT_BROKER = settings.MQTT_BROKER
MQTT_PORT = settings.MQTT_PORT
MQTT_TOPIC = settings.MQTT_TOPIC

@shared_task
def process_mqtt_message(topic, payload):
    """Celery task to process incoming MQTT messages."""
    print(f"Received MQTT message on {topic}: {payload}")
    
    # # Example: Save data to a Django model
    # from .models import SensorData
    # SensorData.objects.create(topic=topic, data=payload)

def on_connect(client, userdata, flags, rc):
    """Called when the client connects to the broker."""
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

def on_disconnect(client, userdata, rc):
    """Handles disconnection and attempts to reconnect."""
    print(f"Disconnected from MQTT Broker (Code: {rc}). Reconnecting...")
    while not client.is_connected():
        try:
            client.reconnect()
            print("Reconnected to MQTT Broker")
            break
        except Exception as e:
            print(f"Reconnection failed: {e}, retrying in 5 seconds...")
            time.sleep(5)

def on_message(client, userdata, msg):
    """Called when a message is received from MQTT."""
    print(f"MQTT Message: {msg.topic} - {msg.payload.decode()}")
    process_mqtt_message.delay(msg.topic, msg.payload.decode())  # Send message to Celery

def start_mqtt_client():
    """Initialize and start the MQTT client with auto-reconnect."""
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    try:
        print(f"Connecting to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()  # Keeps running and handles reconnections
    except Exception as e:
        print(f"Connection error: {e}. Retrying in 5 seconds...")
        time.sleep(5)
        start_mqtt_client()  # Recursive retry on failure
