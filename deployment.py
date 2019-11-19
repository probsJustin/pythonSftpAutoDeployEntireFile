import configparser
import __future__
import os
import socket
import sys
import pysftp
import paramiko
import sys
import logging

config = configparser.ConfigParser()
logging.basicConfig(filename='deployment.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def logThis(logText):
    logging.warning(logText)
    print(logText)


def readConfigurations():
    configurations = dict() 
    try:
        config.read('./deploymentConfig.ini')
    except:
        logThis("Configuration file is not available for some reason.")
   
    configurations = config._sections
    try:
        configurations['config']['remote_server']
    except KeyError:
        logThis("There was a problem with the remote_server configuration.")
        return False
    try:
        configurations['config']['remote_pass']
    except KeyError:
        logThis("There was a problem with the remote_pass configuration.")
        return False
    try:
        configurations['config']['remote_user']
    except KeyError:
        logThis("There was a problem with the remote_user configuration.")
        return False

    if(configurations['config']['remote_server'] == False):
        logThis("remote_server is missing from the configuration file.")
        return False
    if(configurations['config']['remote_user'] == False):
        logThis("remote_user is missing from the configuration file.")
        return False
    if(configurations['config']['remote_pass'] == False):
        logThis("remote_pass is missing from the configuration file.")
        return False
    return configurations


def sftpConnection(host, user, password):
    if(deploymentConfiguration['config']['debug_disable_sftp'] == "False"):
        cnopts = pysftp.CnOpts()
        if cnopts.hostkeys.lookup(host) == None:
            logThis("New host - will accept any host key")
            hostkeys = cnopts.hostkeys
            cnopts.hostkeys = None
    
        with pysftp.Connection(host, user, None ,password, cnopts=cnopts) as sftp:
            logThis("Connection succesfully stablished ... ")
        #this should always be the same
            localFilePath = './'
            if(deploymentConfiguration['config']['remote_pass'] == False):
                remoteFilePath = '/'
            else:
                if(deploymentConfiguration['config']['remote_path'][-1] == '/' or deploymentConfiguration['config']['remote_path'][-1] == '\\'):
                    remoteFilePath = deploymentConfiguration['config']['remote_path']
                else:
                    if(deploymentConfiguration['config']['remote_path'][0] == "/"):
                        remoteFilePath = deploymentConfiguration['config']['remote_path'] + "/"
                    else:
                        if(deploymentConfiguration['config']['remote_path'][0] == "\\"):
                            remoteFilePath = deploymentConfiguration['config']['remote_path'] + "\\"
                        else:
                            remoteFilePath = deploymentConfiguration['config']['remote_path'] + "/"


            for x in os.listdir():
                forLoopLock = False
                for y in deploymentConfiguration['config']['exclude_files'].split(','):
                   if(x == y):
                       forLoopLock = True
                       break
                if(forLoopLock == True): 
                    logThis('File : "' + x + '" has been excluded')
                else:
                    print('File : "' + x + '" has been uploaded')
                    sftp.put(localFilePath + x, remoteFilePath + x)
            try:
                deploymentConfiguration['config']['remote_command']
                
                logThis("command attempting to be sent")
                logThis(deploymentConfiguration['config']['remote_command'])
                sftp.execute(deploymentConfiguration['config']['remote_command'])
            except:
                logThis("No deployment command enabled.")
            
            

    else:
        print("Debug flag enabled will not upload files to sftp remote")
        try:
            if(sys.argv[2] == "github"): 
                logThis("github is enabled")
                github = deploymentConfiguration['config']['push_to_github']
        except:
            github = "False"
            print("We will not push to github") 
            
        if(github == "True"): 
            logThis("attempting to push local repo to github")
            commitMessage = ""
            try:
                sys.argv[1]
                logThis("[GITHUB] Commit message will be: " + sys.argv[1])
                commitMessage = sys.argv[1]
            except:
                commitMessage = "commit message not provided"
                logThis("[GITHUB] Commit message is not provided.")
            for x in os.listdir():
                forLoopLock = False
                for y in deploymentConfiguration['config']['exclude_files'].split(','):
                    if(x == y):
                        forLoopLock = True
                        break
                    if(forLoopLock == True): 
                        logThis('File : "' + x + '" has been excluded')
                    else:
                        try:
                           logThis('File : "' + x + '" has been uploaded')
                           logThis("github : ", os.system("git merge"))
                           logThis("github : ", os.system("git add ./" + x))
                        except:
                           logThis("There was a problem trying to push to github")
            try:
               logThis("github : ", os.system('git commit -m "' + commitMessage + '"'))
               logThis("github : ", os.system("git push"))
            except:
               logThis("There was a problem trying to push to github")
deploymentConfiguration = readConfigurations() 
if(deploymentConfiguration != False):
    logThis("Configuration read successfully.")
    logThis("Will attempt to connect.")
    
    sftpConnection(deploymentConfiguration['config']['remote_server'], deploymentConfiguration['config']['remote_user'],deploymentConfiguration['config']['remote_pass'])
else:
    logThis("Deployment will not continue as there is an error in the configuration.")
