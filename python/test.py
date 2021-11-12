import os
print('\nstarting test')
# META FUNCTIONS

if (not os.path.isdir('rng_tunnel')):
    os.mkdir('rng_tunnel')
if (not os.path.isdir('user_keys')):
    os.mkdir('user_keys')
if (not os.path.isdir('user_proxy')):
    os.mkdir('user_proxy')
if (not os.path.isdir('proxy_user')):
    os.mkdir('proxy_user')
if (not os.path.isdir('proxy_tunnel')):
    os.mkdir('proxy_tunnel')
if (not os.path.isdir('tunnel_proxy')):
    os.mkdir('tunnel_proxy')
if (not os.path.isdir('tunnel_server')):
    os.mkdir('tunnel_server')
if (not os.path.isdir('server_tunnel')):
    os.mkdir('server_tunnel')


# DOWNLOAD KEYS
from keyGenerator import generateKeys # 1
from tunnel import downloadKeys as tunnelDownloadKeys, messageProxy # 2
from tunnel import distributedKey as tunnelDistributeKey # 3
from user import downloadKey as userDownloadKey # 4

def metaDownloadKeys():
    generateKeys(1)
    tunnelDownloadKeys()
    tunnelDistributeKey()
    userDownloadKey()

metaDownloadKeys()

# AUTHENTIFICATE
from user import authUser as userAuth # 1
from proxy import receiveMessageUser as proxyReceiveMessageUser # 2
from tunnel import receiveMessageProxy as tunnelReceiveMessageProxy # 3
from proxy import receiveMessageTunnel as proxyReceiveMessageTunnel # 4
from user import receiveMessageProxy as userReceiveMessageProxy # 5

def metaAuthentificate():
    userAuth()
    proxyReceiveMessageUser()
    tunnelReceiveMessageProxy()
    proxyReceiveMessageTunnel()
    userReceiveMessageProxy()

metaAuthentificate()

# MESSAGE
from user import messageProxy as userMessageProxy # 1
# from proxy import receiveMessageUser as proxyReceiveMessageUser # 2
# from tunnel import receiveMessageProxy as tunnelReceiveMessageProxy # 3
from server import receiveMessageTunnel as serverReceiveMessageTunnel # 4
from tunnel import receiveMessageServer as tunnelReceiveMessageServer # 5
# from proxy import receiveMessageTunnel as proxyReceiveMessageTunnel # 6
# from user import receiveMessageProxy as userReceiveMessageProxy # 7

def metaMessage():
    message = "?"
    userMessageProxy(message)
    proxyReceiveMessageUser()
    tunnelReceiveMessageProxy()
    serverReceiveMessageTunnel()
    tunnelReceiveMessageServer()
    proxyReceiveMessageTunnel()
    userReceiveMessageProxy()

metaMessage()
