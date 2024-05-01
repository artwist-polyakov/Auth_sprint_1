#!/bin/bash

echo "**********************************************"

echo "Starting replicaset initialization..."

echo "Waiting for startup.."
sleep 10

echo SETUP.sh time now: `date +"%T" `

mongosh --host mongo1:27017 --eval "rs.initiate({_id: \"myReplicaSet\", members: [{_id: 0, host: \"mongo1\", \"priority\": 4}, {_id: 1, host: \"mongo2\", \"priority\": 2}, {_id: 2, host: \"mongo3\", \"priority\": 1}]})"

echo "Replica set initialization done."

mongosh --host mongo1:27017 --eval "db.getMongo().setReadPref('primaryPreferred');"
mongosh --host mongo1:27017 --eval "db.getMongo().setReadPref('primary');"
mongosh --host mongo1:27017 --eval "rs.status();"

echo "**********************************************"

