#!/bin/bash

/opt/topicator/topicator -v &>> /var/log/topicator/topicator.log & #> /dev/null 2>&1

echo $! > /var/run/topicator.pid
