import paho.mqtt.client as mqtt
import time

def clock_hands_angle(hours, minutes):
    hours %= 12
    minutes %= 60

    Hour_division_angle = (360/(60 * 12))

    angle_min = (minutes * 6) % 360

    angle_hours = ((hours * 60) + minutes ) * Hour_division_angle

    angle = angle_hours - angle_min

    angle0 = (360 - angle) % 360
    angle1 = (360 - angle0) % 360
    
    return (max(angle0,angle1),min(angle0,angle1))

def on_connect(client, __, flags, rc):
    if rc == 0:
        print("Connected successfully.")
        client.subscribe(Sub_topic1)
    else:
        print("Connect returned result code: " + str(rc))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection. Reconnecting...")
        

def on_message(client, __ , message): 
    print("Received message: " + str(message.payload.decode("utf-8")) + " on topic " + message.topic)
    if message.topic == Sub_topic1:
        try:
            hours, minutes = map(int, message.payload.decode("utf-8").split(":"))
            print(f"Hours: {hours}, Minutes: {minutes}")
            maxangle,minangle = clock_hands_angle(hours, minutes)
            print(f"Max angle {maxangle}, Min angle {minangle}")
            client.publish(Pub_topic1, f"Max angle {maxangle}, Min angle {minangle}",0)
        except ValueError:
            err_message = "Error: Message payload is not in the expected format. Please send time in 'H:M' format."
            print(err_message)
            client.publish(Pub_topic0, err_message,0)
            
            

def on_publish(client, userdata, mid):
    if mid is None:
        print("Message not published.")
    else:
        print("Message published. Message ID: ", mid)
    

def on_log(client, __ , level, buf):
    print("log: ", buf)

broker_address = "192.168.100.94"
broker_port = 9001

Pub_topic0 = "Error"
Pub_topic1 = "Clock_angle"
Sub_topic1 = "Clock_Hours_Minutes(H:M)"




client = mqtt.Client(transport="websockets")
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_log = on_log
client.on_publish = on_publish


max_retries = 10
retry_delay = 5  # delay in seconds

for i in range(max_retries):
    try:
        client.connect(broker_address, broker_port)
        break
    except TimeoutError:
        print(f"Failed to connect to MQTT broker at {broker_address}:{broker_port} over WebSocket. Please check if the broker is running and the address and port are correct.")
        if i < max_retries - 1:  # no need to sleep on the last iteration
            time.sleep(retry_delay)
    except OSError:
        print("Network error occurred. Please check your internet connection.")
        if i < max_retries - 1:  # no need to sleep on the last iteration
            time.sleep(retry_delay)
    except mqtt.MQTTException as e:
        print(f"MQTT error occurred: {e}")
        if i < max_retries - 1:  # no need to sleep on the last iteration
            time.sleep(retry_delay)
else:
    print(f"Failed to connect after {max_retries} attempts. Exiting.")
    exit(1)

client.loop_start()



i = 0
try:
    while True: 
        pass
except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    client.loop_stop()
    print("Client Stopped.")