#!/bin/bash
rm -r $app_path/res/db/weightrpi.db
cp -p $app_path/res/db/weightrpi_new.db $app_path/res/db/weightrpi.db
exit

