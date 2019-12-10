#!/bin/bash

TRAIN=$1 OUTPUT=$2 CBOW=$3 SIZE=$4 WINDOW=$5 NEGATIVE=$6 HS=$7 SAMPLE=$8 THREADS=$9 BINARY=${10} ITER=${11} MIN_COUNT=${12}
LOCAL=${13} USER=${14} USERSERVER=${15} PASSWORD=${16} NODES=${17} CLUSTER=${18} PPN=${19} WALLTIME=${20} EMAIL=${21} TYPE=${22}
 
if [ $LOCAL = 1  ]; then # Local Execution
       
    if [ ! -d "./PLN/wang2vec"  ]; # First Execution
    then
        unzip PLN/wang2vec.zip -d PLN/
        cd PLN/wang2vec/trunk/ && make
        cd ../../../data/ && chmod +x getText8.sh && ./getText8.sh && cd ..
    fi
    cd PLN/wang2vec/trunk && ./word2vec -train ../../../data/$TRAIN -output ../$OUTPUT -type $TYPE -cbow $CBOW -size $SIZE -window $WINDOW -negative $NEGATIVE -hs $HS -sample $SAMPLE -threads $THREADS -binary $BINARY -iter $ITER -min-count $MIN_COUNT

else 
    # External Execution
    sshpass -p $PASSWORD ssh $USERSERVER "
        if [ ! -d "'./wrapper/PLN/wang2vec'"  ]; # First Execution
            then
                unzip wrapper/PLN/wang2vec.zip -d wrapper/PLN/
                cd wrapper/PLN/wang2vec/trunk/ && make
                cd ../../../data && chmod +x getText8.sh && ./getText8.sh && cd ../../
        fi "

    sshpass -p $PASSWORD ssh $USERSERVER "gcc wrapper/PLN/wang2vec/trunk/word2vec.c -o wrapper/PLN/wang2vec/trunk/wang2vec -lm -pthread -O3 -march=native -Wall -funroll-loops -Wno-unused-result"

    #Writing Script file in the server
    sshpass -p $PASSWORD ssh $USERSERVER "{ echo '#!/bin/bash' > wrapper/PLN/wang2vec/trunk/script.sh;} 
                                          { echo 'gcc word2vec.c -o word2vec -lm -pthread -O3 -march=native -Wall -funroll-loops -Wno-unused-result' &>> wrapper/PLN/wang2vec/trunk/script.sh;} 
                                          { echo './word2vec -train ../../../data/$TRAIN -output $OUTPUT -type $TYPE -cbow $CBOW -size $SIZE -window $WINDOW -negative $NEGATIVE -hs $HS -sample $SAMPLE -threads $THREADS -binary $BINARY -iter $ITER ' &>> wrapper/PLN/wang2vec/trunk/script.sh;}"
    sshpass -p $PASSWORD ssh $USERSERVER " chmod 777 wrapper/PLN/wang2vec/trunk/script.sh;"

    #Writing Batchjob file
    sshpass -p $PASSWORD ssh $USERSERVER "
    { echo '#!/bin/bash' > wrapper/PLN/wang2vec/trunk/Batchjob;} 
    { echo '#PBS -m abe' &>> wrapper/PLN/wang2vec/trunk/Batchjob;} 
    { echo '#PBS -V' &>> wrapper/PLN/wang2vec/trunk/Batchjob;} 
    { echo '#PBS -l nodes=$NODES:cluster-$CLUSTER:ppn=$PPN,walltime=$WALLTIME' &>> wrapper/PLN/wang2vec/trunk/Batchjob;} 
    { echo '#PBS -M  $EMAIL' &>> wrapper/PLN/wang2vec/trunk/Batchjob;} 
    { echo '#PBS -r n' &>> wrapper/PLN/wang2vec/trunk/Batchjob;} 
    { echo '#PBS -j oe' &>> wrapper/PLN/wang2vec/trunk/Batchjob;} 
    { echo '#PBS -d /home/$USER/wrapper/PLN/wang2vec/trunk/' &>> wrapper/PLN/wang2vec/trunk/Batchjob;} 
    { echo 'echo Running on host \`hostname\`' &>> wrapper/PLN/wang2vec/trunk/Batchjob;} 
    { echo 'echo Initial Time is \`date\`' &>> wrapper/PLN/wang2vec/trunk/Batchjob;} 
    { echo 'echo Directory is \`pwd\`'&>> wrapper/PLN/wang2vec/trunk/Batchjob;}
    { echo 'echo This jobs runs on the following nodes:' &>> wrapper/PLN/wang2vec/trunk/Batchjob;} 
    { echo 'echo \`cat \$PBS_NODEFILE | uniq\`' &>> wrapper/PLN/wang2vec/trunk/Batchjob;} 
    { echo 'echo JOB_ID:' &>> wrapper/PLN/wang2vec/trunk/Batchjob;} 
    { echo 'echo \`echo '\`'echo' '\$PBS_JOBID'\`'\`'&>> wrapper/PLN/wang2vec/trunk/Batchjob;} 
    { echo 'echo' &>> wrapper/PLN/wang2vec/trunk/Batchjob;} 
    { echo './script.sh' &>> wrapper/PLN/wang2vec/trunk/Batchjob;} 
    { echo 'echo' &>> wrapper/PLN/wang2vec/trunk/Batchjob;} 
    { echo 'echo Final Time is \`date\`' &>> wrapper/PLN/wang2vec/trunk/Batchjob;} "

    sshpass -p $PASSWORD ssh $USERSERVER "/usr/local/torque-4.2.9/bin/qsub wrapper/PLN/wang2vec/trunk/Batchjob "
fi