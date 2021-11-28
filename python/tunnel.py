import os # is used to read / write files and navigate folders
import json # is used to parse json files
from typeEnum import Type # type of message

# GLOBAL VARIABLES ##############################################################################################################

userKeyDictionnary = {}
keyList = []
lastKeyIndexAssinged = 0

# KEY MANAGEMENT FUNCTIONS ######################################################################################################

# check if there are unread keyfiles and attributes a key id before placing them into the keyList
def downloadKeys():
    keyIndex = 0
    for _ in os.listdir("rng_tunnel"):
        with open("rng_tunnel/key" + str(keyIndex) + ".json", "r") as keyFile:
            keyJSON = json.loads(str(keyFile.read()))
            keyList.append(keyJSON["key"])
        os.remove("rng_tunnel/key" + str(keyIndex) +".json")
        keyIndex += 1

# keeps track of the last index of key distributed
def distributedKey():
    global lastKeyIndexAssinged
    with open("user_keys/key.json", "w") as keyFile:
            keyJSON = json.dumps({
                'key':keyList[lastKeyIndexAssinged]
            })
            keyFile.write(keyJSON)

# panic mode
def deleteKeys():
    keyIndex = 0
    for _ in os.listdir("rng_tunnel"):
        os.remove("rng_tunnel/key" + str(keyIndex) +".json")
    keyIndex += 1
    keyList.clear()

# RECEIVE FUNCTIONS #############################################################################################################

# receives a message from the server
def receiveMessageServer():
   if (os.path.exists("server_tunnel/message.json")):
        with open("server_tunnel/message.json", "r") as messageFile:
            messageJSON = json.loads(str(messageFile.read()))
            messageJSON["type"] = Type.MSG.value
            messageProxy(messageJSON)
        os.remove("server_tunnel/message.json")


# recevies message by proxy
def receiveMessageProxy():
   if (os.path.exists("proxy_tunnel/message.json")):
        with open("proxy_tunnel/message.json", "r") as messageFile:
            messageJSON = json.loads(str(messageFile.read()))
            if (messageJSON["type"] == Type.AUTH.value):
                authUser(messageJSON)
            elif (messageJSON["type"] == Type.MSG.value):
                messageServer(messageJSON)
            elif (messageJSON["type"] == Type.DISC.value):
                disconnectUser(messageJSON)
        os.remove("proxy_tunnel/message.json")

# authentificate user
def authUser(messageJSON):
    success = False
    for key in keyList:
        if (key[0: 3: 1] == messageJSON["body"]):
            userKeyDictionnary[messageJSON["userId"]] = keyList.index(key)
            success = True
    if (success):
        with open("tunnel_proxy/message.json", "w") as messageFile:
            messageJSON["body"] = "success"
            messageFile.write(json.dumps(messageJSON))
    else:
        with open("tunnel_proxy/message.json", "w") as messageFile:
            messageJSON["body"] = "failure"
            messageFile.write(json.dumps(messageJSON))

# disconnect user
def disconnectUser(messageJSON):
    if (userKeyDictionnary[messageJSON["userId"]] is not None):
        with open("tunnel_proxy/message.json", "w") as messageFile:
            messageJSON["body"] = "success"
            messageFile.write(json.dumps(messageJSON))
        userKeyDictionnary.pop(messageJSON["userId"])
    else:
        with open("tunnel_proxy/message.json", "w") as messageFile:
            messageJSON["body"] = "failure"
            messageFile.write(json.dumps(messageJSON))

    
# MESSAGE FUNCTIONS #############################################################################################################

# decrypts a message from the proxy and sends it to the server
def messageServer(messageJSON):
    messageJSON["body"] = crypt(messageJSON)
    messageJSON.pop("type")
    with open("tunnel_server/message.json", "w") as messageFile:
        messageFile.write(json.dumps(messageJSON))

# encrypt a message from the server and sends it to the proxy
def messageProxy(messageJSON):
    messageJSON["body"] = crypt(messageJSON)
    with open("tunnel_proxy/message.json", "w") as messageFile:
        messageFile.write(json.dumps(messageJSON))

# performs XOR operation on two strings
def crypt(messageJSON):
    global keyList
    key = keyList[userKeyDictionnary[messageJSON["userId"]]] 
    newMessage = "".join([chr(ord(a) ^ ord(b)) for a,b in zip(key, messageJSON["body"])])
    keyList[userKeyDictionnary[messageJSON["userId"]]] = keyList[userKeyDictionnary[messageJSON["userId"]]][len(messageJSON["body"]): len(keyList[userKeyDictionnary[messageJSON["userId"]]])]
    return newMessage