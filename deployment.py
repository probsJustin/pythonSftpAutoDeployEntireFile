import configparser
import os
import pysftp
import sys
import logging
import traceback

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
                if(x in deploymentConfiguration['config']['exclude_files'].split(',')):

                    logThis('File : "' + x + '" has been excluded')
                else:
                    print('File : "' + x + '" has been uploaded')
                    sftp.put(localFilePath + x, remoteFilePath + x)
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
    except Exception as error: 
        logThis(error)
else:
    logThis("Deployment will not continue as there is an error in the configuration.")
