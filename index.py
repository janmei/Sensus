import requests
import paho.mqtt.client as mqtt
import pygame
import os
import pathlib
import socket
import platform

system = platform.system()

if system == "Linux":
    device_id = socket.gethostname()
    mqtt_topic = "section/%s/#" % device_id
    song21 = '/home/pi/fred/music.ogg'
    song22 = '/home/pi/fred/News-Sound.wav'
    song23 = '/home/pi/fred/music.ogg'
    pass
elif system == "Darwin":
    device_id = os.getenv("SECTION_ID")
    mqtt_topic = "section/%s/#" % device_id
    song1 = '/Applications/XAMPP/xamppfiles/htdocs/fred/music.ogg'
    song2 = '/Applications/XAMPP/xamppfiles/htdocs/fred/News-Sound.wav'
    song3 = '/Applications/XAMPP/xamppfiles/htdocs/fred/music.ogg'
    pass
print(mqtt_topic)

songid = ""

pygame.init()
sound1 = pygame.mixer.Sound(song1)
sound2 = pygame.mixer.Sound(song2)
sound3 = pygame.mixer.Sound(song3)

if device_id == '1':
    lightid = 3
    pass
if device_id == '2':
    lightid = 18
    pass
if device_id == '3':
    lightid = 19
    pass

if device_id == '4':
    lightid = 20
    pass


def startRequest(data):

    url = "http://192.168.0.20/api/vWOsvVaprpwthxcEnlbcxVjhU6deEL1JV7X8PnXj/lights/" + str(lightid) + "/state"
    payload = data
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data = payload)

    print(str(response.text, "utf-8"))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = str(msg.payload, "utf-8")
    # print(topic)
    if topic == "section/" + device_id + "/lamp":
        startRequest(payload)
        pass
    elif topic == "section/" + device_id + "/song":
        songid = payload
        print(songid)
        pass
    elif topic == "section/" + device_id + "/song/play":

        print(payload)

        if payload == "1":
            sound1.stop()
            sound1.play()
            pass
        elif payload == "2":
            sound2.stop()
            sound2.play()
            pass
        elif payload == "3":
            sound2.stop()
            sound2.play()
            pass
        pass
    elif topic == "section/" + device_id + "/song/pause":
        # sound.pause()
        print("Pause")
        print(payload)
        pass
    elif topic == "section/" + device_id + "/song/volume":
        # sound.set_volume(float(payload)/100)
        print(payload)
        pass

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.188.20", 1883, 60)

client.loop_forever()


