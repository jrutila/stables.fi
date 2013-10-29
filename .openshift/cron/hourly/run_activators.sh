#!/bin/sh
source $OPENSHIFT_HOMEDIR/python/virtenv/bin/activate
python $OPENSHIFT_REPO_DIR/wsgi/openshift/manage.py tenant_activators

