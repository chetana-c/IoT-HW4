import logging
import time
import yaml
import paho.mqtt.client as mqtt


def current_milli_time():
    return round(time.time_ns())


global config, secrets
with open('config.yml', 'r') as config_file:
    global config
    config = yaml.safe_load(config_file)
with open(config['secrets_file'], 'r') as secrets_file:
    global secrets
    secrets = yaml.safe_load(secrets_file)

BROKER_HOSTNAME = config['broker']['hostname']
BROKER_PORT = config['broker']['port']
CREDS = secrets['credentials']['mqtt_users'][1]
AUTO_RECONNECT_DELAY = 20
AUTO_RECONNECT_RETRIES = 100
KEEPALIVE = 60
REFRESH_RATE = 0.1

IMU_SENSOR_TOPIC = config['topics']['imu_sensor']

reconnect_flag = True
kill_flag = False

logging.basicConfig(filename='logs/mqtt_sub.csv', format='%(asctime)s.%(msecs)03d,%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', filemode='w+')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# function for
def mqtt_sub():
    """MQTT Subscriber"""

    print("Starting as MQTT Subscriber...")

    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print(f"Connected to '{BROKER_HOSTNAME}:{BROKER_PORT}' as '{client._client_id.decode('utf-8')}'.")
            client.subscribe(topic=IMU_SENSOR_TOPIC, qos=2)
        else:
            print(
                f"Failed to connect to '{BROKER_HOSTNAME}:{BROKER_PORT}' as '{client._client_id.decode('utf-8')}'. Retrying...")

    def reconnect(client):

        if AUTO_RECONNECT_DELAY > 0:
            print(f"Auto-reconnecting in {AUTO_RECONNECT_DELAY} seconds...")
            client.reconnect_flag = True

    def on_disconnect(client, userdata, reasonCode, properties):
        if reasonCode == 0:
            print(f"Disconnected from '{BROKER_HOSTNAME}:{BROKER_PORT}' as '{client._client_id.decode('utf-8')}'.")
            reconnect(client)
        else:
            print(
                f"Disconnected due reasonCode {reasonCode} from '{BROKER_HOSTNAME}:{BROKER_PORT}' as '{client._client_id.decode('utf-8')}'. Retrying...")

        client.kill_flag = True

    def on_message(client, userdata, message):
        print(message.topic, ":", message.payload.decode())

    rpi_client = mqtt.Client(client_id='mqtt_sub', protocol=mqtt.MQTTv5)
    rpi_client.kill_flag = False
    rpi_client.reconnect_flag = True
    rpi_client.enable_logger(logger=logging.Logger('mqtt_sub'))
    rpi_client.username_pw_set(username=CREDS['username'], password=CREDS['password'])
    rpi_client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
    rpi_client.on_connect = on_connect
    rpi_client.on_disconnect = on_disconnect
    rpi_client.on_message = on_message
    rpi_client.change_flag = False

    try:
        rpi_client.connect(host=BROKER_HOSTNAME, port=BROKER_PORT, keepalive=KEEPALIVE)
    except Exception as e:
        print("Unable to connect to host." + str(e))
        return False
    print("Starting connection...")
    rpi_client.loop_start()

    while not rpi_client.is_connected() and not rpi_client.kill_flag:
        # wait to connect or kill
        time.sleep(REFRESH_RATE)

    while rpi_client.is_connected() and not rpi_client.kill_flag:
        # wait to disconnect or kill
        # publish here
        time.sleep(REFRESH_RATE)

    del rpi_client
    return reconnect_flag


# mqtt_sub()
while AUTO_RECONNECT_RETRIES > 0:
    mqtt_sub()
    time.sleep(AUTO_RECONNECT_DELAY)
    AUTO_RECONNECT_RETRIES -= 1
