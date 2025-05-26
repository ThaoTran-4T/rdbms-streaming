import pandas as pd
import json
from kafka import KafkaProducer

# df = pd.read_csv('VNI-test.csv')
df = pd.read_csv('IOT-temp.csv')


BOOTSTRAP_SERVER = 'localhost:9092'
TOPIC = 'temperature'

producer = KafkaProducer(security_protocol="PLAINTEXT", bootstrap_servers=BOOTSTRAP_SERVER)
col = []
for i in range(0, 5):
    col.append(df.columns[i])

def send(tmp):
    '''s = ""
    for i in range(0,6):
        s = s + col[i] + ": " + str(tmp[i]) + "-"'''
    s = {}
    for i in range(0, 5):
        if i == 3:
            s[col[i]] = int(tmp[i])
        else:
            s[col[i]] = tmp[i]
    print("Message: ", s)
    producer.send(TOPIC, value = json.dumps(s).encode('utf-8'))

import time
timing = 3
for i in range(df.shape[0]-1, -1, -1):
    tmp = list(df.loc[i])
    send(tmp)
    time.sleep(timing)