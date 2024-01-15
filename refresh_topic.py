from selenium import webdriver
import paho.mqtt.client as mqtt
import yaml
import time

global config, secrets
with open('config.yml', 'r') as config_file:
    global config
    config = yaml.safe_load(config_file)
with open(config['secrets_file'], 'r') as secrets_file:
    global secrets
    secrets = yaml.safe_load(secrets_file)


def on_message(client, userdata, msg):
    new_status = msg.payload.decode()

    print(f"Received new status: {new_status}")

    if new_status.lower() == 'refresh':
        driver.refresh()


client = mqtt.Client(client_id="client-2")
client.on_message = on_message
client.connect(config['broker']['hostname'], config['broker']['port'], 60)

client.subscribe("status_change", qos=1)

client.loop_start()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("executable_path=/path/to/chromedriver.exe")

driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome(executable_path="C:\\chromedriver.exe")
driver.implicitly_wait(0.5)

driver.get("http://127.0.0.1:5000/")
while True:
    time.sleep(1)
    driver.refresh()
