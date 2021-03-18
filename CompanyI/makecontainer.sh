#!/usr/bin/env bash
# A small script to create a Docker container
# Script is verified to work on Fedora Linux only

DOCKER=$(command -v docker)

if [ "$UID" -ne 0  ]; then
    echo "Program needs elated privileges."
    exit 1
fi

if [ -z "$DOCKER" ]; then
    echo "Cannot continue as docker executable is not in the path"
    exit 1
else
    systemctl start docker
fi

echo "Step 1: == Building the Docker container =="
docker build -t tech-task .

echo "Step 2: == Saving the Docker container =="
docker save -o tech-task.tar tech-task

echo "Step 3: == Loading the newly created container =="
docker load -i tech-task.tar

echo "Step 4: == Testing the loaded container =="
echo "Test satellite catalog number is 150 and days are 10"
echo
docker run tech-task 150 10
