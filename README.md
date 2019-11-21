# pythonSftpAutoDeployEntireFile

A script that can be placed in the base of any repo and be ran to upload to a test server as well commit to the local repo.

Automate the deployment of your application to your remote test server.

Think of this as your deployment buddy! This is a python script that you can place in the base of your repo and have it run and do 3 things: upload everything in this file to your remote server except for excluded items with in the configuration, run a command on your remote server to put changes into effect if needed and commit to your local repo as well as push. 

Note: The local repo must be initialized and have an initial commit to allow for this to work correctly. 

### Reason: 

I could see a bunch of things that claimed to use sftp and ssh to push things remotely to a set server but the ones that I had found were pretty shotty and or confusing to configure correctly. It seemed like a good idea to write one out that allows for a single command to push to github and remote locations as well as run a command to make the changes. 

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
add pem key authentication to allow for users to use keys as well for authentication
