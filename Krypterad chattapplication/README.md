# Chat Application with MQTT and Encryption, create by Isaac Skog

## Introduction
This project implements a chat application that uses the MQTT protocol to send and receive encrypted messages between participants. The program utilizes symmetric encryption, meaning all participants share the same encryption key. 

## Features
1. **Encryption and Decryption**: Messages are encrypted using Fernet (a type of symmetric encryption) before sending and decrypted upon receipt.
2. **Chat Rooms**: Users can select a chat room and connect to a specific MQTT topic.
3. **Passphrase-based Key Generation**: An encryption key is generated based on a passphrase provided by the user at startup.

## System Requirements
- Python
- Libraries:+
  - `paho-mqtt`
  - `cryptography`

## Installation
Install the required dependencies by running the following command on git bash for windows:

Create a new virtual environment
```bash
python -m venv .venv
```
Activate the virtual environment
```bash
source .venv/Scripts/activate
```
```bash
pip install cryptography
```
```bash
pip install paho-mqtt 
```

## Usage
1. Start the program:

   ```bash
   python chatt-skal.py
   ```

2. Enter a username.
3. Enter a passphrase to generate the encryption key.
4. Select a chat room to join.
5. Type messages to send them encrypted to all other participants in the chat room.
6. Exit the program by typing `quit`.

## Code Overview
### Key Classes and Functions

#### **Chat**
- **`__init__`**: Initializes the chat with a username, chat room, and a passphrase.
- **`create_key`**: Generates an encryption key from a passphrase using SHA-256 and Base64.
- **`connect_mqtt`**: Sets up the MQTT connection and subscribes to the chosen chat room.
- **`on_message`**: Decrypts and prints incoming messages.
- **`run`**: The main loop that sends and encrypts messages.

#### **Main**
- Responsible for gathering user input and starting the chat application.

## Key Details
- Fernet encryption requires a 32-byte key. The program generates this from a passphrase using a SHA-256 hash, which is Base64-encoded.
- MQTT messages are sent and received as encrypted byte strings.

## Example
```plaintext
Enter your username: isaac
Enter passphrase to generate encryption key: secret123
Pick a room:
        python
> python
isaac > Connected with result code 0
hello, how are you
isaac > movantchat/python b'gAAAAABnWtziB2LolXoUZf1s74XTsBcXtzWZml7LQP0n1fMzyZj8PdbpctVR2LhHsoq1Wu_YRjLevlGMM0NOfOsjRRr9xxlLcABwejESgRvvMuXLTQvk7Pg=' -> hello, how are you
```

## References
- [Paho MQTT Client Documentation](https://www.eclipse.org/paho/index.php?page=clients/python/index.php)
- [Cryptography Library](https://cryptography.io/en/latest/fernet/)