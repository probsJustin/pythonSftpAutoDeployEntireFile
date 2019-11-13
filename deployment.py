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
        # Backup loaded .ssh/known_hosts file
        hostkeys = cnopts.hostkeys
        # And do not verify host key of the new host
        cnopts.hostkeys = None
    
    with pysftp.Connection(host, user, None ,password, cnopts=cnopts) as sftp:
        print("Connection succesfully stablished ... ")

    # Define the file that you want to upload from your local directorty
    # or absolute "C:\Users\sdkca\Desktop\TUTORIAL2.txt"
        localFilePath = './testFile.txt'

    # Define the remote path where the file will be uploaded
        remoteFilePath = '/test/testFile.txt'

        sftp.put(localFilePath, remoteFilePath)

deploymentConfiguration = readConfigurations() 
if(deploymentConfiguration != False):
    print("Configuration read successfully.")
    print("Will attempt to connect.")
    
    sftpConnection(deploymentConfiguration['config']['remote_server'], deploymentConfiguration['config']['remote_user'],deploymentConfiguration['config']['remote_pass'])
else:
    print("Deployment will not continue as there is an error in the configuration.")
