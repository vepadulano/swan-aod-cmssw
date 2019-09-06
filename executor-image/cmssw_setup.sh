#!/bin/sh
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700
scramv1 project CMSSW_11_0_ROOT618_X_2019-08-28-2300
cd CMSSW_11_0_ROOT618_X_2019-08-28-2300
eval `scramv1 runtime -sh`
