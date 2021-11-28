import os
import json

# GLOBAL VARAIBLES ##############################################################################################################

# MESSAGE FUNCTIONS #############################################################################################################

def messageTunnel(messageJSON):
    with open("server_tunnel/message.json", "w") as messageFile:
            messageFile.write(messageJSON)

# RECEIVE MESSAGE FUNCTIONS #####################################################################################################

def receiveMessageTunnel():
    if (os.path.exists("tunnel_server/message.json")):
        with open("tunnel_server/message.json", "r") as messageFile:
            messageJSON = json.loads(str(messageFile.read()))
            serve(messageJSON)
        os.remove("tunnel_server/message.json")

# SERVE #########################################################################################################################

def serve(messageJSON):
    answer = {
        'userId': messageJSON["userId"]
    }
    if (len(messageJSON["body"].split(' ')) == 2):
        operand = messageJSON["body"].split(' ')[0]
        operator =  messageJSON["body"].split(' ')[1]
        if operand == "cf":
            open("server_root_directory/" + operator, "w")
            answer["body"] = "file created successfully"
        elif operand == "of":
            if os.path.exists("server_root_directory/" +  operator):
                file = open("server_root_directory/" + operator, 'r')
                answer["body"] = "nano" + file.read()
            else:
                answer["body"] = "file does not exist successfully"
        else:
            answer["body"] = "unrecognized command" + operand
    else:
        answer["body"] = "bad request"
    
    answerJSON =json.dumps(answer)
    messageTunnel(answerJSON)

# TEST ##########################################################################################################################

# messageJSONTest = {
#     'userId': 12,
#     'body': 'cd kmd'
# }
# serve(messageJSONTest)