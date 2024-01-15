import paho.mqtt.client as mqtt
from flask import Flask, render_template
import yaml

app = Flask(__name__)

global config, secrets
with open('config.yml', 'r') as config_file:
    global config
    config = yaml.safe_load(config_file)
with open(config['secrets_file'], 'r') as secrets_file:
    global secrets
    secrets = yaml.safe_load(secrets_file)

broker_url = config['broker']['hostname']
broker_port = config['broker']['port']

client = mqtt.Client(client_id="client-1")
client.username_pw_set(secrets['credentials']['mqtt_users'][0]['username'],
                       secrets['credentials']['mqtt_users'][0]['password'])

client.connect(broker_url, broker_port)


def on_message(client, userdata, msg):
    status = msg.payload.decode()

    f = open("status.txt", "w")
    f.write(status)
    f.close()

    print(status)

    client.publish("status_change", payload=status, qos=1, retain=True)
client.on_message = on_message

# Subscribe
topic = config['topics']['imu_sensor']
client.subscribe(topic)


@app.route('/', methods=['GET', 'POST'])
def index():
    f = open("status.txt", "r")
    status = f.read()
    return render_template('index.html', status=status)


if __name__ == '__main__':
    app.run(debug=True)