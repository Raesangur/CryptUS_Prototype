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
        if (operand == 'cd'):
            answer["body"] = changeDirectory(operator)
    else:
        answer["body"] = 'bad request'
    
    answerJSON =json.dumps(answer)
    messageTunnel(answerJSON)

def changeDirectory(operator):
    if (os.path.isdir('server_root_directory/' + operator)):
        body = ''
        for file in os.listdir('server_root_directory/' + operator):
            body += file + '\t'
        return body
    elif (os.path.isfile('server_root_directory/' + operator)):
        return 'not a directory'
    else:
        return 'no such file in directory ' + operator

# TEST ##########################################################################################################################

# messageJSONTest = {
#     'userId': 12,
#     'body': 'cd kmd'
# }
# serve(messageJSONTest)