# pythonSftpAutoDeployEntireFile
A script that can be placed in the base of any repo and be ran to upload to a test server as well commit to the local repo.

Automate the deployment of your application to your remote test server.

Think of this as your deployment buddy! This is a python script that you can place in the base of your repo and have it run and do 3 things: upload everything in this file to your remote server except for excluded items with in the configuration, run a command on your remote server to put changes into effect if needed and commit to your local repo as well as push. 

Note: The local repo must be initialized and have an initial commit to allow for this to work correctly. 

# Config file options
[config]
#required

exclude_files = deploymentConfig.ini,deployment.pyproj,deployment.py,env,.git,.gitignore,.gitattributes

#comma separated list of files to exclude in the containing directory 

remote_server = remote address
  
remote_user = remote username
  
remote_pass = remote user password
  

#optional

#note that remote_path will default to '/'

remote_path = path that you want to upload to (note that this needs to include a '/' at the end) 
  
debug_disable_sftp = (True or False)

push_to_github = (True or False)

remote_command = remote command to be executed on your server

## TODO: 
add more error handling for configurations to stop people from messing it up. 

Requirements: 
pystfp (version 0.2.9) 
