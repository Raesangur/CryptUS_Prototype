import os
import json

# GLOBAL VARAIBLES ##############################################################################################################

# MESSAGE FUNCTIONS #############################################################################################################

def messageTunnel(messageJSON):
    with open("server_tunnel/message.json", "w") as messageFile: # open in readonly mode
            messageFile.write(messageJSON)

# RECEIVE MESSAGE FUNCTIONS #####################################################################################################

def receiveMessageTunnel():
    if (os.path.exists("tunnel_server/message.json")):
        with open("tunnel_server/message.json", "r") as messageFile: # open in readonly mode
            messageJSON = json.loads(str(messageFile.read()))
            serve(messageJSON)
        os.remove("tunnel_server/message.json")

# SERVE #########################################################################################################################

def serve(messageJSON):
    answer = {
        'userId': messageJSON["userId"]
    }
    if (messageJSON["body"] == "?"):
        answer["body"] = "!"
    else:
        answer["body"] = "?"
    answerJSON =json.dumps(answer)
    messageTunnel(answerJSON)