import threading
from django.apps import AppConfig
from .tasks import start_mqtt_client


class VitalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vitals'

    def ready(self):
        mqtt_thread = threading.Thread(target=start_mqtt_client, daemon=True)
        mqtt_thread.start()
     # register tasks
     
