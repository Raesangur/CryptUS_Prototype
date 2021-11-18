import os
import json
from typeEnum import Type

# GLOBAL VARAIBLES ##############################################################################################################

key = ''
ip = '192.192.192.192'
connected = False

# KEY MANAGEMENT FUNCTIONS ######################################################################################################

# downloads a new key for the user to use
def downloadKey():
    global key
    with open("user_keys/key.json", "r") as keyFile:
            key = json.loads(str(keyFile.read()))["key"]
    os.remove("user_keys/key.json")

# delete his own key
def deleteKey():
    global key
    key = ''

# XOR on a message
def crypt(message):
    global key
    if (len(message) > len(key)):
        print('\n\tcannot encrypt or decrypt the message due to the key length, session terminated')
        exit()
    newMessage = "".join([chr(ord(a) ^ ord(b)) for a,b in zip(key, message)])
    key = key[len(message):len(key)]
    return newMessage

# MESSAGE FUNCTIONS #############################################################################################################

# sends message to proxy
def messageProxy(body):
    if (connected):
        messageJSON = json.dumps({
            'ip': ip,
            'type': Type.MSG.value,
            'body': crypt(body)
        }, indent = 4)

        with open("user_proxy/message.json", "w") as messageFile:
                messageFile.write(messageJSON)
    else:
        print('\n\tplease authentificate yourself before sending messages')

# authentification of the user
def authUser():
    global key
    if (not connected):
        messageJSON = json.dumps({
            'ip': ip,
            'type': Type.AUTH.value,
            'body': key[0: 3: 1]
        })
        with open("user_proxy/message.json", "w") as messageFile:
                messageFile.write(messageJSON)
    else:
        print('\n\tyou are already connected')

def disconnect():
    global key
    if (connected):
        messageJSON = json.dumps({
            'ip': ip,
            'type': Type.DISC.value,
            'body': ''
        }, indent = 4)
        with open("user_proxy/message.json", "w") as messageFile:
            messageFile.write(messageJSON)
    else:
        print('\n\tyou are not connected')

# RECVEIVE MESSAGE FUNCTIONS ####################################################################################################

# treats messages received from proxy
def receiveMessageProxy():
    global connected
    if (os.path.exists("proxy_user/message.json")):
        with open("proxy_user/message.json", "r") as messageFile:
            messageJSON = json.loads(str(messageFile.read()))
            if (messageJSON["type"] == Type.MSG.value):
                messageJSON["body"] = crypt(messageJSON["body"])
                print('\n\t' + messageJSON["body"])
            if (messageJSON["type"] == Type.AUTH.value):
                if (messageJSON["body"] == "success"):
                    connected = True
                    print('\n\tconnection successful')
                else:
                    connected = False
                    print('\n\tfailed to connect')
            if (messageJSON["type"] == Type.DISC.value):
                if (messageJSON["body"] == "success"):
                    connected = False
                    print('\n\tdisconnected successfully')
                else:
                    connected = True
                    print('\n\tfailed to disconnect')
        os.remove("proxy_user/message.json")