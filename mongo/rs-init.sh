#!/bin/bash

echo "**********************************************"

echo "Starting replicaset initialization..."

echo "Waiting for startup.."
sleep 10

echo SETUP.sh time now: `date +"%T" `

mongosh --host mongo1:27017 --eval "rs.initiate({ \n
 _id: \"myReplicaSet\", \n
 members: [ \n
   {_id: 0, host: \"mongo1\", \"priority\": 4}, \n
   {_id: 1, host: \"mongo2\", \"priority\": 2}, \n
   {_id: 2, host: \"mongo3\", \"priority\": 1} \n
 ] \n
})"

echo "Replica set initialization done."

mongosh --host mongo1:27017 --eval "db.getMongo().setReadPref('primaryPreferred');"
mongosh --host mongo1:27017 --eval "db.getMongo().setReadPref('primary');"
mongosh --host mongo1:27017 --eval "rs.status();"

echo "**********************************************"

