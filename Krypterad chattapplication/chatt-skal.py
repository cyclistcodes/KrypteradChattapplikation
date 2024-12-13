import random
import base64
from cryptography.fernet import Fernet
from hashlib import sha256

try:
    import paho.mqtt.client as paho
except ModuleNotFoundError:
    print("Error: The 'paho.mqtt.client' module is not available!")
    exit(1)

CLIENT_ID = f'movant-mqtt-{random.randint(0, 1000)}'
USERNAME = ''
PASSWORD = ''
BROKER = 'broker.hivemq.com'
PORT = 1883

CHAT_ROOMS = {
    'python': 'movantchat/python'
}

class Chat:
    def __init__(self, username, room, passphrase):
        self.username = username
        self.room = room
        self.topic = CHAT_ROOMS[room]
        self.client = None
        self.key = self.create_key(passphrase)  # Encryption key from passphrase
        self.cipher = Fernet(self.key)  # Fernet cipher object
        self.connect_mqtt()
        self.running = True

    def create_key(self, passphrase):
        
        key = sha256(passphrase.encode('utf-8')).digest()  # Create a SHA-256 hash of the passphrase
        return base64.urlsafe_b64encode(key)  # Return the base64 encoded key

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code", rc)

    def connect_mqtt(self):
        
        self.client = paho.Client(CLIENT_ID)
        self.client.username_pw_set(USERNAME, PASSWORD)
        self.client.on_connect = self.on_connect
        self.client.connect(BROKER, PORT, 120)
        self.client.subscribe(self.topic)
        self.client.on_message = self.on_message
        self.client.loop_start()

    def on_message(self, client, userdata, msg):
        
        try:
            decrypted_msg = self.cipher.decrypt(msg.payload).decode('utf-8')
            print(f"{msg.topic} {msg.payload} -> {decrypted_msg}")
        except Exception as e:
            print(f"Failed to decrypt message: {e}")

    def run(self):
        
        try:
            while self.running:
                msg_to_send = input(f"{self.username} > ")  

                if msg_to_send.lower() == "quit":
                    
                    self.client.publish(self.topic, self.cipher.encrypt(f"{self.username} left the chat".encode('utf-8')))
                    self.running = False
                    break

                encrypted_msg = self.cipher.encrypt(msg_to_send.encode('utf-8'))  # Encrypt the message
                self.client.publish(self.topic, encrypted_msg)
        except KeyboardInterrupt:
            print("Exiting chat...")
        finally:
            self.client.loop_stop()
            self.client.disconnect()


def main():
    
    username = input("Enter your username: ")
    passphrase = input("Enter passphrase to generate encryption key: ")

    print("Pick a room:")
    for room in CHAT_ROOMS:
        print(f"\t{room}")

    while True:
        room = input("> ")
        if room in CHAT_ROOMS:
            break
        print("Invalid room. Please try again.")

    chat = Chat(username, room, passphrase)
    chat.run()


if __name__ == '__main__':
    main()