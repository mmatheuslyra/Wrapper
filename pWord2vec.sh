#!/bin/bash

TRAIN=$1 OUTPUT=$2 CBOW=$3 SIZE=$4 WINDOW=$5 NEGATIVE=$6 HS=$7 SAMPLE=$8 THREADS=$9 BINARY=${10} ITER=${11} MIN_COUNT=${12}
LOCAL=${13} USER=${14} USERSERVER=${15} PASSWORD=${16} NODES=${17} CLUSTER=${18} PPN=${19} WALLTIME=${20} EMAIL=${21} BATCH_SIZE=${22}

if [ $LOCAL != '0' ]; then # Local Execution
    if [ ! -d "./PLN/pWord2Vec"  ]; # First Execution
    then
        unzip PLN/pWord2Vec.zip -d PLN/
        make PLN/pWord2Vec/
        cd data/ && chmod +x getText8.sh && ./getText8.sh && cd ../PLN/pWord2Vec/
    fi

    ./pWord2Vec -train data/$TRAIN -output $OUTPUT -size $SIZE -window $WINDOW -negative $NEGATIVE -sample $SAMPLE -threads $THREADS -binary $BINARY -iter $ITER -min-count $MIN_COUNT -batch-size $BATCH_SIZE
else # External Execution

    sshpass -p $PASSWORD ssh $USERSERVER "
        if [ ! -d "'./wrapper/PLN/pWord2vec'"  ]; # First Execution
            then
                unzip wrapper/PLN/pWord2vec.zip -d wrapper/PLN/
                cd wrapper/PLN/pWord2vec/ && make
                cd ../../../data && chmod +x getText8.sh && ./getText8.sh && cd ../../
        fi "

    sshpass -p $PASSWORD ssh $USERSERVER "gcc wrapper/PLN/pWord2vec/pWord2vec.c -o wrapper/PLN/pWord2vec/pWord2vec -lm -pthread -O3 -march=native -Wall -funroll-loops -Wno-unused-result"

    #Writing Script file in the server
    sshpass -p $PASSWORD ssh $USERSERVER "{ echo '#!/bin/bash' > wrapper/PLN/pWord2vec/script.sh;} 
                                          { echo 'gcc pWord2vec.c -o pWord2vec -lm -pthread -O3 -march=native -Wall -funroll-loops -Wno-unused-result' &>> wrapper/PLN/pWord2vec/script.sh;} 
                                          { echo './pWord2vec -train ../../../data/$TRAIN -output $OUTPUT -cbow $CBOW -size $SIZE -window $WINDOW -negative $NEGATIVE -hs $HS -sample $SAMPLE -threads $THREADS -binary $BINARY -iter $ITER ' &>> wrapper/PLN/pWord2vec/script.sh;}"
    sshpass -p $PASSWORD ssh $USERSERVER " chmod 777 wrapper/PLN/pWord2vec/script.sh;"

    #Writing Batchjob file
    sshpass -p $PASSWORD ssh $USERSERVER "
    { echo '#!/bin/bash' > wrapper/PLN/pWord2vec/Batchjob;} 
    { echo '#PBS -m abe' &>> wrapper/PLN/pWord2vec/Batchjob;} 
    { echo '#PBS -V' &>> wrapper/PLN/pWord2vec/Batchjob;} 
    { echo '#PBS -l nodes=$NODES:cluster-$CLUSTER:ppn=$PPN,walltime=$WALLTIME' &>> wrapper/PLN/pWord2vec/Batchjob;} 
    { echo '#PBS -M  $EMAIL' &>> wrapper/PLN/pWord2vec/Batchjob;} 
    { echo '#PBS -r n' &>> wrapper/PLN/pWord2vec/Batchjob;} 
    { echo '#PBS -j oe' &>> wrapper/PLN/pWord2vec/Batchjob;} 
    { echo '#PBS -d /home/$USER/wrapper/PLN/pWord2vec/' &>> wrapper/PLN/pWord2vec/Batchjob;} 
    { echo 'echo Running on host \`hostname\`' &>> wrapper/PLN/pWord2vec/Batchjob;} 
    { echo 'echo Initial Time is \`date\`' &>> wrapper/PLN/pWord2vec/Batchjob;} 
    { echo 'echo Directory is \`pwd\`'&>> wrapper/PLN/pWord2vec/Batchjob;}
    { echo 'echo This jobs runs on the following nodes:' &>> wrapper/PLN/pWord2vec/Batchjob;} 
    { echo 'echo \`cat \$PBS_NODEFILE | uniq\`' &>> wrapper/PLN/pWord2vec/Batchjob;} 
    { echo 'echo JOB_ID:' &>> wrapper/PLN/pWord2vec/Batchjob;} 
    { echo 'echo \`echo '\`'echo' '\$PBS_JOBID'\`'\`'&>> wrapper/PLN/pWord2vec/Batchjob;} 
    { echo 'echo' &>> wrapper/PLN/pWord2vec/Batchjob;} 
    { echo './script.sh' &>> wrapper/PLN/pWord2vec/Batchjob;} 
    { echo 'echo' &>> wrapper/PLN/pWord2vec/Batchjob;} 
    { echo 'echo Final Time is \`date\`' &>> wrapper/PLN/pWord2vec/Batchjob;} "

    sshpass -p $PASSWORD ssh $USERSERVER "/usr/local/torque-4.2.9/bin/qsub wrapper/PLN/pWord2vec/Batchjob "
fi