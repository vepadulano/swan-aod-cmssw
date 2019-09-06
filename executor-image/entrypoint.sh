#!/bin/bash
source /cmssw_setup.sh
/bin/bash ${SPARK_HOME}/kubernetes/dockerfiles/spark/entrypoint.sh "$@"
