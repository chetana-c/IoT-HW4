# Homeword Assignment - 4
_Group-4 Submission_

## Installation (for Linux ONLY)
1. Clone git repo and navigate into project's root directory
   ```shell
   git clone https://github.com/UntitledError-09/csc591-iot_hw4.git
   cd csc591-iot_hw4
   ```
2. Setup python virtual environment
   ```shell
   conda create -n csc591-iot-hw4 python3==3.11
   ```
3. Activate python virtual environment (VERY IMPORTANT; has to be run before )
   ```shell
   # to activate environment
   conda activate csc591-iot-hw4
   # to deactivate environment
   conda deactivate
   ```
4. Install python dependencies
   ```shell
   # conda activate csc591-iot-hw4
   pip install -U -r requirements.txt
   ```
5. Setup broker for MQTT ([HiveMQ](https://console.hivemq.cloud/))
   * Login and create new cluster (free cluster will suffice)
   * Configure users in [Access Management Console](https://console.hivemq.cloud/) (https://console.hivemq.cloud/clusters/free/<your_cluster_id>/credentials)
6. Configure the clients info by editing [secrets.yml](secrets.yml) in the following format:
    ```text
    credentials:
        mqtt_users:
            - username: <username>
              password: <password>
            - username: <username>
              password: <password>
    ```
   
## Running Tests
### MQTT Clients:
2. **Raspberry Pi (Publisher)** at [**rpi**.py](rpi.py)
   ```shell
   # conda activate csc591-iot-hw4
   python3 mqtt_pub.py # mqtt_pub.py
   # once script starts, a prompt appears for each sub-task
   # default 'Yes' (Only Return is considered 'Yes')
   # exits program after all four tests are completed
   ```
3. **Laptop (Subscriber)** at [**laptop**.py](laptop.py)
   ```shell
   # conda activate csc591-iot-hw4
   python3 mqtt_sub.py # mqtt_sub.py
   # this just keeps running and logging
   ```
4. Get logs in [logs](logs)
