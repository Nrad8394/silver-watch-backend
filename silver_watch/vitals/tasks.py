import json
import time
import paho.mqtt.client as mqtt
from celery import shared_task
from django.conf import settings
from django.utils import timezone

MQTT_BROKER = settings.MQTT_BROKER
MQTT_PORT = settings.MQTT_PORT
MQTT_TOPIC = settings.MQTT_TOPIC
DEVICE_STATUS_TOPIC = "device/status"  # Topic for device status updates
CONNECTED_DEVICES = {}  # Dictionary to track connected devices and their last activity

@shared_task
def process_mqtt_message(topic, payload):
    """Celery task to process incoming MQTT messages."""
    print(f"Received MQTT message on {topic}: {payload}")
    
    # Process the incoming data from MQTT
    try:
        import json
        from django.contrib.auth import get_user_model
        from .models import VitalSigns
        from devices.models import Device
        
        # Parse the JSON payload
        data = json.loads(payload)
        
        # Track device connectivity if this is a data message
        device_id = data.get("device_id")
        if device_id:
            update_device_status(device_id, "Online")
        
        # Process vital signs data
        user_id = data.get("user_id")
        if user_id:
            User = get_user_model()
            try:
                user = User.objects.get(id=user_id)
                
                # Create a new VitalSigns record
                vitals = VitalSigns(
                    patient=user,
                    heart_rate=data.get("heart_rate", 0),
                    heart_rate_status="Normal",  # You might want to add logic to determine this
                    blood_pressure_systolic=data.get("systolicBP", 0),
                    blood_pressure_diastolic=data.get("diastolicBP", 0),
                    blood_pressure_status="Normal",  # Add logic for this
                    temperature=data.get("temperature", 0),
                    temperature_status="Normal",  # Add logic for this
                    blood_oxygen=data.get("spo2", 0),
                    blood_oxygen_status="Normal",  # Add logic for this
                    respiratory_rate=0,  # Not provided in the data
                    respiratory_rate_status="Normal",
                    consciousness_value=0,  # Not provided in the data
                    consciousness_status="Normal"
                )
                vitals.save()
                
                print(f"Saved vital signs for user {user.username}")
                
            except User.DoesNotExist:
                print(f"User with ID {user_id} not found")
    except Exception as e:
        print(f"Error processing MQTT message: {str(e)}")

def update_device_status(device_id, status):
    """Update device status in the database and connection tracker"""
    try:
        from devices.models import Device
        
        # Update the device status in our tracking dictionary
        CONNECTED_DEVICES[device_id] = {
            'status': status,
            'last_seen': timezone.now()
        }
        
        # Also update the device status in the database
        device = Device.objects.filter(id=device_id).first()
        if device:
            previous_status = device.status
            device.status = status
            if status == "Online":
                print(f"Device {device_id} is now online")
            elif status == "Offline" and previous_status != "Offline":
                print(f"Device {device_id} went offline")
            device.save()
        else:
            print(f"Device with ID {device_id} not found in database")
    except Exception as e:
        print(f"Error updating device status: {str(e)}")

@shared_task
def check_device_connectivity():
    """Periodically check device connectivity and update offline status"""
    try:
        from devices.models import Device
        offline_threshold = timezone.now() - timezone.timedelta(minutes=5)
        
        # Update database for devices that haven't reported in 5 minutes
        for device_id, info in CONNECTED_DEVICES.items():
            if info['status'] == "Online" and info['last_seen'] < offline_threshold:
                update_device_status(device_id, "Offline")
                
        # Also check for devices in DB that might be missing from our tracker
        for device in Device.objects.filter(status="Online"):
            if device.id not in CONNECTED_DEVICES or CONNECTED_DEVICES[device.id]['last_seen'] < offline_threshold:
                update_device_status(device.id, "Offline")
                
    except Exception as e:
        print(f"Error in device connectivity check: {str(e)}")

def on_connect(client, userdata, flags, rc):
    """Called when the client connects to the broker."""
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(MQTT_TOPIC)
        client.subscribe(f"{DEVICE_STATUS_TOPIC}/#")  # Subscribe to all device status topics
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
    topic = msg.topic
    payload = msg.payload.decode()
    
    # Handle device status messages
    if topic.startswith(DEVICE_STATUS_TOPIC):
        try:
            data = json.loads(payload)
            device_id = data.get("device_id")
            status = data.get("status")
            if device_id and status:
                update_device_status(device_id, status)
            return
        except json.JSONDecodeError:
            print(f"Invalid JSON in device status message: {payload}")
    
    # Process regular data messages
    process_mqtt_message.delay(topic, payload)

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