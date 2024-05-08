#!/bin/bash

./opt/topicator/topicator -d info &>> /var/log/topicator/topicator.log & #> /dev/null 2>&1

echo $! > /var/run/topicator.pid
