import smbus #import SMBus module of 12C
import numpy as np
import pickle
from time import sleep
import paho.mqtt.client as mqtt

PWR_MGM_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG =0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H=0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H =0x45
GYRO_ZOUT_H = 0x47

bus=smbus.SMBus (1) 
Device_Address=0x68
fdir = "model"
svm_path = fdir+"svm.pkl"

def MPU_Init():

    bus.write_byte_data (Device_Address, SMPLRT_DIV, 7)
    bus.write_byte_data (Device_Address, PWR_MGM_1, 1)
    bus.write_byte_data (Device_Address, CONFIG, 0)
    bus.write_byte_data (Device_Address, GYRO_CONFIG, 24)
    bus.write_byte_data (Device_Address, INT_ENABLE, 1)

def read_raw_data (addr):

    high= bus.read_byte_data (Device_Address, addr)
    low= bus.read_byte_data (Device_Address, addr+1)
    value = ((high << 8) | low)
    if (value > 32768):
        value = value - 65536
    return value

def load_model(model_path):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

MPU_Init()
current_state = "CLOSED"

def read_values():
    #MPU6050 device address
    #Read Accelerometer raw value
    acc_x = read_raw_data (ACCEL_XOUT_H)
    acc_y= read_raw_data (ACCEL_YOUT_H)
    acc_z = read_raw_data (ACCEL_ZOUT_H)

    #Read Gyroscope raw value
    gyro_x= read_raw_data (GYRO_XOUT_H)
    gyro_y= read_raw_data (GYRO_YOUT_H)
    gyro_z = read_raw_data (GYRO_ZOUT_H)
    Ax = acc_x/16384.0
    Ay =acc_y/16384.0
    Az= acc_z/16384.0

    Gx= gyro_x/131.0
    Gy= gyro_y/131.0
    Gz = gyro_z/131.0

    print ("Gx=%.2f" %Gx, "Gy=%.2f" %Gy, "Gz=%.2f " %Gz, "Ax=%.2f g" %Ax, "Ay=%.2f g" %Ay, "Az=%.2f g" %Az)

    return Az, Gy

svm_model = load_model(svm_path)

client = mqtt.Client("mqtt-client-1")

while True:

    Gy_vals = []
    Az_vals = []
    sleep (1)
    for _ in range(5):
        sleep(0.2)
        Az, Gy = read_values()
        Az_vals.append(Az)
        Gy_vals.append(Gy)

    Az_curr = max(Az_vals) if current_state == "CLOSED" else min(Az_vals)
    Gy_curr = min(Gy_vals) if current_state == "CLOSED" else max(Gy_vals)

    np_input = np.array([Gy_curr, Az_curr]).reshape(1, -1)
    state = svm_model.predict(np_input)[0]
    print(state)

    if state != current_state and state != "IDLE":
        print(f"State changed from {current_state} to {state}")
        new_state = {"state":state}
        client.publish("imu-sensor", payload = new_state, qos = 2)
        current_state = state
    else:    
        print(f"No state change, current state {current_state}")
