#!/bin/bash

echo Running on host `hostname`
echo Initial Time is `date`
echo Directory is `pwd`
echo This jobs runs on the following nodes:
echo `cat $PBS_NODEFILE | uniq`
echo JOB_ID:
echo `echo $PBS_JOBID`
echo
./script.sh
echo
echo Final Time is `date`

