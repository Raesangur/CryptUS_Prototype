import os
print('\nstarting test')

# CREATING DIRECTORIES ##########################################################################################################

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
if (not os.path.isdir('server_root_directory')):
    os.mkdir('server_root_directory')

# META FUNCTIONS ################################################################################################################

# DOWNLOAD KEYS #################################################################################################################

from keyGenerator import generateKeys # 1
from tunnel import downloadKeys as tunnelDownloadKeys, messageProxy # 2
from tunnel import distributedKey as tunnelDistributeKey # 3
from user import downloadKey as userDownloadKey # 4

def metaDownloadKeys():
    generateKeys(1)
    tunnelDownloadKeys()
    tunnelDistributeKey()
    userDownloadKey()

# metaDownloadKeys()

# AUTHENTIFICATE ################################################################################################################

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

# metaAuthentificate()

# MESSAGE #######################################################################################################################

from user import messageProxy as userMessageProxy # 1
# from proxy import receiveMessageUser as proxyReceiveMessageUser # 2
# from tunnel import receiveMessageProxy as tunnelReceiveMessageProxy # 3
from server import receiveMessageTunnel as serverReceiveMessageTunnel # 4
from tunnel import receiveMessageServer as tunnelReceiveMessageServer # 5
# from proxy import receiveMessageTunnel as proxyReceiveMessageTunnel # 6
# from user import receiveMessageProxy as userReceiveMessageProxy # 7

def metaMessage():
    message = "cd ddkemnjknde"
    userMessageProxy(message)
    proxyReceiveMessageUser()
    tunnelReceiveMessageProxy()
    serverReceiveMessageTunnel()
    tunnelReceiveMessageServer()
    proxyReceiveMessageTunnel()
    userReceiveMessageProxy()

# metaMessage()

# CLI ###########################################################################################################################

from user import disconnect as userDisc

userInput = ''
while (userInput != 'fq'):

    # MENU

    print('\nthis is a cli bip bop\n')
    print('\tgks -- generate keys\n')
    print('\tkey -- download a new key\n')
    print('\tauth -- authentificate\n')
    print('\tdc -- disconect\n')
    print('\tre -- request\n')
    print('\tfq -- force quit\n')
    userInput = input('\tinput: ')

    # KEY GENERATION

    if (userInput == 'gks'):
        isValidNum = False
        while (not isValidNum):
            try:
                userInput = input('\n\thow many keys do you want to create ? [0 - 100]: ')
                if (len(str(userInput).split(' ')) == 1):
                    if(int(userInput) > -1 and int(userInput) < 101):
                        isValidNum = True
                    else:
                        print('\n\twrong input')
                else:
                    print('\n\twrong input')
            except:
                print('\n\twrong input')
                userInput = '-1'
        generateKeys(int(userInput))
        tunnelDownloadKeys()
    
    # KEY DOWNLOAD

    if (userInput == 'key'):
        userInput = ''
        while (userInput != 'y' and userInput != 'n'):
            userInput = input('\n\tif there are no key available this will generate an error and the program will terminate, proceed ? [y/n]: ')
            if (userInput == 'y'):
                tunnelDistributeKey()
                userDownloadKey()
            elif (userInput != 'n'):
                print('\n  wrong input')

    # AUTHENTIFICATE

    if (userInput == 'auth'):
        userAuth()
        proxyReceiveMessageUser()
        tunnelReceiveMessageProxy()
        proxyReceiveMessageTunnel()
        userReceiveMessageProxy()

    # REQUEST

    if (userInput == 're'):
        userInput = input("\n\tenter your request to the server: ")
        userMessageProxy(str(userInput))
        proxyReceiveMessageUser()
        tunnelReceiveMessageProxy()
        serverReceiveMessageTunnel()
        tunnelReceiveMessageServer()
        proxyReceiveMessageTunnel()
        userReceiveMessageProxy()
        userInput = ''

    # DISCONNECT

    if (userInput == 'dc'):
        while (userInput != 'y' and userInput != 'n'):
            userInput = input('\n\tyou are about to disconect, proceed ? [y/n]: ')
            if (userInput == 'y'):
                userDisc()
                proxyReceiveMessageUser()
                tunnelReceiveMessageProxy()
                proxyReceiveMessageTunnel()
                userReceiveMessageProxy()
            elif (userInput != 'n'):
                print('\n\twrong input')
