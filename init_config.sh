#!/bin/bash -x
supervisorctl start celery
supervisorctl start celery_beat

b2share demo load_config
b2share db init
b2share upgrade run -v
