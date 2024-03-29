#!/bin/bash
# Backs up the OpenShift PostgreSQL database for this application
# by Skye Book <skye.book@gmail.com>
 
NOW="$(date +"%Y-%m-%d")"
FILENAME="$OPENSHIFT_DATA_DIR/backup/$OPENSHIFT_APP_NAME.$NOW.backup.sql.gz"
pg_dump $OPENSHIFT_APP_NAME | gzip > $FILENAME
