#!/bin/bash
rm -r $app_path/res/db/truckid.dat
cd $app_path/res/db
chmod 777 truckid.dat
hostname > truckid.dat
chmod 444 truckid.dat
exit

