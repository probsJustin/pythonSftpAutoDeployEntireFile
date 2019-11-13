import configparser
import __future__
import os
import socket
import sys
import pysftp
import paramiko

config = configparser.ConfigParser()

def readConfigurations():
    configurations = dict() 
    try:
        config.read('./deploymentConfig.ini')
    except:
        print("Configuration file is not available for some reason.")
    configurations = config._sections
    try:
        configurations['config']['remote_server']
    except KeyError:
        print("There was a problem with the remote_server configuration.")
        return False
    try:
        configurations['config']['remote_pass']
    except KeyError:
        print("There was a problem with the remote_pass configuration.")
        return False
    try:
        configurations['config']['remote_user']
    except KeyError:
        print("There was a problem with the remote_user configuration.")
        return False

    if(configurations['config']['remote_server'] == False):
        print("remote_server is missing from the configuration file.")
        return False
    if(configurations['config']['remote_user'] == False):
        print("remote_user is missing from the configuration file.")
        return False
    if(configurations['config']['remote_pass'] == False):
        print("remote_pass is missing from the configuration file.")
        return False
    return configurations


def sftpConnection(host, user, password):
        cnopts = pysftp.CnOpts()
        if cnopts.hostkeys.lookup(host) == None:
            print("New host - will accept any host key")
            hostkeys = cnopts.hostkeys
            cnopts.hostkeys = None
    
        with pysftp.Connection(host, user, None ,password, cnopts=cnopts) as sftp:
            print("Connection succesfully stablished ... ")
        #this should always be the same
            localFilePath = './'
            if(deploymentConfiguration['config']['remote_pass'] == False):
                remoteFilePath = '/'
            else:
                remoteFilePath = deploymentConfiguration['config']['remote_path']

            for x in os.listdir():
                forLoopLock = False
                for y in deploymentConfiguration['config']['exclude_files'].split(','):
                   if(x == y):
                       forLoopLock = True
                       break
                if(forLoopLock == True): 
                    print('File : "' + x + '" has been excluded')
                else:
                    print('File : "' + x + '" has been uploaded')
                    sftp.put(localFilePath + x, remoteFilePath + x)
                
deploymentConfiguration = readConfigurations() 
if(deploymentConfiguration != False):
    print("Configuration read successfully.")
    print("Will attempt to connect.")
    
    sftpConnection(deploymentConfiguration['config']['remote_server'], deploymentConfiguration['config']['remote_user'],deploymentConfiguration['config']['remote_pass'])
else:
    print("Deployment will not continue as there is an error in the configuration.")
