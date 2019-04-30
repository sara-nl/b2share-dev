#!/bin/bash -x
supervisorctl start celery
supervisorctl start celery_beat

sleep 20

b2share index destroy
b2share index init
b2share index run
b2share index reindex --yes-i-know
b2share index run

