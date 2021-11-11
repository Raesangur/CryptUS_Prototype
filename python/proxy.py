import json
import os
from typeEnum import Type # type of message

# GLOBAL VARAIBLES ##############################################################################################################

userList = ["ERREUR"] # liste des utilisateurs avec le IP en fonction du userID

# USER MANAGEMENT FUNCTIONS #####################################################################################################

# fonction qui ajoute un utilisateur en fonction de son IP. Retourne son ID.
def addUser(userIP):
    if userIP in userList:
        return 0
    else:
        userList.append(userIP)
        return len(userList)-1

# fonction qui retire un utilisateur en fonction de son id
def removeUserID(userID):
    if (len(userList)-1)>= userID:
        userList.pop(userID)
        return True
    else:
        return False

# fonction qui retire un utilisateur en fonction de son ip
def removeUserIP(userIP):
    if userIP in userList:
        oldUserIndex = userList.index(userIP)
        userList.remove(userIP)
        return oldUserIndex
    else:
        return 0

# fonction qui retourne l'IP en fonction de l'ID
def getIP(userID):
    if (len(userList)-1)>= userID:
        return userList[userID]
    else:
        return userList[0]

# fonction qui retourne l'ID en fonction de l'IP
def getID(userIP):
    if userIP in userList:
        return userList.index(userIP)
    else:
        return 0

# MESSAGE FUNCTIONS #############################################################################################################

# sends a message to the tunnel
def messageTunnel(messageJSON):
    messageToTunnelJSON = json.dumps({
        'userId': userList.index(messageJSON["ip"]),
        'type': messageJSON["type"],
        'body': messageJSON["body"]
    }, indent = 4)
    with open("proxy_tunnel/message.json", "w") as messageFile:
            messageFile.write(messageToTunnelJSON)

# sends the authentification to the tunnel or call errors if the user already exists
def authUser(messageJSON):
    if (getID(messageJSON["ip"]) == 0):
        userIndex = addUser(messageJSON["ip"])
    else:
        return authError(messageJSON)
    messageToTunnelJSON = json.dumps({
        'userId': userIndex,
        'type': messageJSON["type"],
        'body': messageJSON["body"]
    }, indent = 4)
    with open("proxy_tunnel/message.json", "w") as messageFile:
            messageFile.write(messageToTunnelJSON)

# sends error to the user
def authError(messageJSON):
    if ("ip" in messageJSON.keys()):
        messageToUserJSON = json.dumps({
            'ip': messageJSON["ip"],
            'type': Type.AUTH.value,
            'body': 'failure'
        }, indent = 4)
    else:
        messageToUserJSON = json.dumps({
            'ip': getIP(messageJSON["userId"]),
            'type': Type.AUTH.value,
            'body': 'failure'
        }, indent = 4)
    with open("proxy_user/message.json", "w") as messageFile:
                messageFile.write(messageToUserJSON)

def disconnect(messageJSON):
    userIndex = removeUserIP(messageJSON["ip"])
    messageToTunnelJSON = json.dumps({
        'userId': userIndex,
        'type': messageJSON["type"]
    }, indent = 4)
    with open("proxy_tunnel/message.json", "w") as messageFile:
            messageFile.write(messageToTunnelJSON)

def disconnectError(messageJSON):
    if ("ip" in messageJSON.keys()):
        messageToUserJSON = json.dumps({
            'ip': messageJSON["ip"],
            'type': Type.DISC.value,
            'body': 'failure'
        }, indent = 4)
    else:
        messageToUserJSON = json.dumps({
            'ip': getIP(messageJSON["userId"]),
            'type': Type.DISC.value,
            'body': 'failure'
        }, indent = 4)
    with open("proxy_user/message.json", "w") as messageFile:
                messageFile.write(messageToUserJSON)
    return
    
# sends message to user
def messageUser(messageJSON):
    messageToTunnelJSON = json.dumps({
        'ip': getIP(messageJSON["userId"]),
        'type': messageJSON["type"],
        'body': messageJSON["body"]
    }, indent = 4)
    with open("proxy_user/message.json", "w") as messageFile:
            messageFile.write(messageToTunnelJSON)

# RECEVIE FUNCTIONS #############################################################################################################

# reads message from tunnel and treats it
def receiveMessageTunnel():
    if (os.path.exists("tunnel_proxy/message.json")):
        with open("tunnel_proxy/message.json", "r") as messageFile:
            messageJSON = json.loads(str(messageFile.read()))
            if (messageJSON["type"] == Type.AUTH.value):
                if (messageJSON["body"] == "success"):
                    messageUser(messageJSON)
                else:
                    authError(messageJSON)
                    removeUserID(messageJSON["userId"])
            elif (messageJSON["type"] == Type.MSG.value):
                messageUser(messageJSON)
            elif (messageJSON["type"] == Type.DISC.value):
                if (messageJSON["body"] == "success"):
                    messageUser(messageJSON)
                else:
                    disconnectError(messageJSON)
        os.remove("tunnel_proxy/message.json")

# reads message from user and treats it
def receiveMessageUser():
    if (os.path.exists("user_proxy/message.json")):
        with open("user_proxy/message.json", "r") as messageFile:
            messageJSON = json.loads(str(messageFile.read()))
            if (messageJSON["type"] == Type.AUTH.value):
                authUser(messageJSON)
            elif (messageJSON["type"] == Type.MSG.value):
                if (getID(messageJSON["ip"]) == 0):
                    authError(messageJSON)
                else:
                    messageTunnel(messageJSON)
            else:
                if (getID(messageJSON["ip"]) != 0):
                    disconnect(messageJSON)
                else:
                    disconnectError(messageJSON)
        os.remove("user_proxy/message.json")