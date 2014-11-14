Visualization frontend for brain connectivity data
========

Author: renaud.richardet@epfl.ch

### Install on OpenShift

Create app:

    rhc app create connectivity -t diy-0.1 --from-code=https://github.com/renaud/brainconnectivity-openshift
    cd connectivity

Your application 'connectivity' is now available.

    URL:        http://connectivity-brainer.rhcloud.com/
    
Follow instructions from README_OLD to add my pip packages from within virtualenv

    rm -rf misc
    virtualenv -p /usr/bin/python2.6 --no-site-packages misc/virtenv
    source misc/virtenv/bin/activate
    pip install PyMySQL simplejson tornado
    deactivate
    git commit...

### MySQL

Go to https://openshift.redhat.com/app/console/applications, click on 'add MySQL'

MySQL 5.5 database added.  Please make note of these credentials:

    Root User: xxx
    Root Password: xxx
    Database Name: connectivity
    Connection URL: mysql://$OPENSHIFT_MYSQL_DB_HOST:$OPENSHIFT_MYSQL_DB_PORT/

    mysql -uxxx -pxxx
    CREATE DATABASE 20140226_coocs;
    CREATE USER 'x'@'%' IDENTIFIED BY 'x';
    GRANT ALL PRIVILEGES ON 20140226_coocs.* TO 'x'@'%' WITH GRANT OPTION;

### Import data

    cd app-root/repo/diy/sql/
    unzip 20141114-brain_connectivity.zip
    mysql -uxxx -pxxx --local-infile
    source table_jsre.sql

### LOGS

1. SSH into my gear rhc ssh
2. Change directory into my logs directory `cd $OPENSHIFT_LOG_DIR`
3. List the contents ls

