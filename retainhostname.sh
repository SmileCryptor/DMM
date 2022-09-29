#!/bin/bash
cd $app_path/res/db
sed -i -e "s/truckid = .*/truckid = "$HOSTNAME""$NULL"/g" config.ini
exit

