import configparser
import os
import pysftp
import sys
import logging
import traceback
from pathlib import Path

#By: Justin Hagerty 2019
#Next Task: add pem keys to allow for better authentication. 

config = configparser.ConfigParser()
logging.basicConfig(filename='deployment.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def logThis(logText):
    logFile(logText)
    print(logText)

def logFile(logText):
    logging.warning(logText)


def readConfigurations():
    configurations = dict() 
    returnOption = True
    try:
        config.read('./deploymentConfig.ini')
    except Exception as error:
        logFile(error)
        logFile(traceback.format_exc())
        logThis("Configuration file is not available for some reason.")
   
    configurations = config._sections
    checks = ['remote_pass','remote_user','remote_server']
    for check in checks: 
        if check not in configurations['config'].keys():
            print(f"{check} is not in the configuration file")
            returnOption = False
        if not configurations.get('config').get(check):
            print(f"{check} is missing a value in the configuration file")
            returnOption = False
    return (returnOption if not returnOption else configurations)


def sftpConnection(host, user, password):
    if(deploymentConfiguration['config']['debug_disable_sftp'] == "False"):
        cnopts = pysftp.CnOpts()
        if cnopts.hostkeys.lookup(host) == None:
            logThis("New host - will accept any host key")
            hostkeys = cnopts.hostkeys
            cnopts.hostkeys = None
            logThis("Connecting to : " + str(host))
        if(deploymentConfiguration['config']['remote_auth_settings'] == "pem" and Path(deploymentConfiguration['config']['local_pem_path']).exists()):
            if(os.path.splitext(Path(deploymentConfiguration['config']['local_pem_path']))[1] == '.pem'):
                print("Supported key identified. This will attempt to connect if this .pem file is not a key it will break.")
                try:
                    with pysftp.Connection(host, user, deploymentConfiguration['config']['local_pem_path']) as sftp:
                        logThis("Connection succesfully stablished ... ")
                        #this should always be the same
                        localFilePath = './'
                        if(deploymentConfiguration['config']['remote_path'] == False):
                            deploymentConfiguration['config']['remote_path'] = '/'
                        else:
                            deploymentConfiguration['config']['remote_path'] = str(Path(deploymentConfiguration['config']['remote_path']))
                            print(deploymentConfiguration['config']['remote_path'])

                        for x in os.listdir():
                            if(x in deploymentConfiguration['config']['exclude_files'].split(',')):
                                logThis('File : "' + x + '" has been excluded')
                            else:
                                print('File : "' + x + '" has been uploaded')
                                sftp.put(localFilePath + x, deploymentConfiguration['config']['remote_path'] + x)
                        try:
                            deploymentConfiguration['config']['remote_command']
       
                            logThis("command attempting to be sent")
                            logThis(deploymentConfiguration['config']['remote_command'])
                            sftp.execute(deploymentConfiguration['config']['remote_command'])
                        except Exception as error:
                            logFile(error)
                            logFile(traceback.format_exc())
                            logThis("No deployment command enabled.")
 
                
                except AttributeError: 
                    print("error") 
                except:
                    logThis("This is likely due to a missing PEM file.") 
                    logThis("We tried to get the pem key at : " + str(deploymentConfiguration['config']['local_pem_path']))
            else:
                print("This is not a supported key.") 
        else:
            if not (Path(deploymentConfiguration['config']['local_pem_path']).exists()):
                logThis("PEM key does not exist - attempting to connect with password")
            with pysftp.Connection(host, user, None ,password, cnopts=cnopts) as sftp:
                logThis("Connection succesfully stablished ... ")
                #this should always be the same
                localFilePath = './'
                if(deploymentConfiguration['config']['remote_path'] == False):
                    deploymentConfiguration['config']['remote_path'] = '/'
                else:
                    if(Path(deploymentConfiguration['config']['remote_path']).exists()):
                        deploymentConfiguration['config']['remote_path'] = str(Path(deploymentConfiguration['config']['remote_path']))
                        logThis("Setting log path as : " + str(deploymentConfiguration['config']['remote_path']))

                for x in os.listdir():
                    if(x in deploymentConfiguration['config']['exclude_files'].split(',')):
                        logThis('File : "' + x + '" has been excluded')
                    else:
                        print('File : "' + x + '" has been uploaded')
                        sftp.put(localFilePath + x, deploymentConfiguration['config']['remote_path'] + x)
                try:
                    deploymentConfiguration['config']['remote_command']
       
                    logThis("command attempting to be sent")
                    logThis(deploymentConfiguration['config']['remote_command'])
                    sftp.execute(deploymentConfiguration['config']['remote_command'])
                except Exception as error:
                    logFile(error)
                    logFile(traceback.format_exc())
                    logThis("No deployment command enabled.")
            
            

    else:
        print("Debug flag enabled will not upload files to sftp remote")
        try:
            if(sys.argv[2] == "github"): 
                logThis("github is enabled")
                github = deploymentConfiguration['config']['push_to_github']
        except Exception as error:
            github = "False"
            logFile(error)
            logFile(traceback.format_exc())
            print("We will not push to github")
            
        if(github == "True"): 
            logThis("attempting to push local repo to github")
            commitMessage = ""
            try:
                sys.argv[1]
                logThis("[GITHUB] Commit message will be: " + sys.argv[1])
                commitMessage = sys.argv[1]
            except Exception as error:
                commitMessage = "commit message not provided"
                logThis("[GITHUB] Commit message is not provided.")
                logFile(traceback.format_exc())
            for x in os.listdir():
                if(x in deploymentConfiguration['config']['exclude_files'].split(',')): 
                    logThis('File : "' + x + '" has been excluded')
                else:
                    try:
                        logThis('File : "' + x + '" has been uploaded')
                        logThis("github : " + os.system("git merge"))
                        logThis("github : " + os.system("git add ./" + x))
                    except Exception as error:
                        logThis("There was a problem trying to push to github")
                        logFile(traceback.format_exc())
                        logFile(error)
            try:
               logThis("github : ", os.system('git commit -m "' + commitMessage + '"'))
               logThis("github : ", os.system("git push"))
            except Exception as error:
                logFile(error)
                logFile(traceback.format_exc())
                logThis("There was a problem trying to push to github")

deploymentConfiguration = readConfigurations() 

if(deploymentConfiguration != False):
    logThis("Configuration read successfully.")
    logThis("Will attempt to connect.")
    try:
        sftpConnection(deploymentConfiguration['config']['remote_server'], deploymentConfiguration['config']['remote_user'],deploymentConfiguration['config']['remote_pass'])
    except AttributeError:
        logThis("Handled")
        logFile(traceback.format_exc())

        pass
    except Exception as error: 
        logThis(error)
        pass
else:
    logThis("Deployment will not continue as there is an error in the configuration.")
