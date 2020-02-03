#!/bin/bash

## Run
# sudo cp -f photobooth-exec.bash /bin/
## Then
#  sudo chmod 744 /bin/photobooth-exec.bash

docker container stop street_photo_flask
# starts the server
cd ~/Documents/projects/photobooth-py/docker
docker-compose up -d

# starts the photobooth app
cd ~/Documents/projects/photobooth-py/software
python main.py