#!/bin/bash

## Run
# sudo cp -f photobooth-exec.bash /bin/
## Then
#  sudo chmod 744 /bin/photobooth-exec.bash

# starts the server
cd ~/Documents/projects/photobooth-py/docker
docker-compose up -d

# starts the photobooth app
cd ~/Documents/projects/photobooth-py
python main.py