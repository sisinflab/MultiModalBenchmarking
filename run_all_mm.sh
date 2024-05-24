#!/bin/bash

cd /home/matteo/Formal-Multimod-Rec
python3 config_templates_test.py --dataset $1 --batch_size $2

cd /home/matteo/Ducho

PYTHONPATH=. python3 ./demos/demo_$1/run.py > ./ducho_log.txt

cd /home/matteo/Ducho/local/data/demo_$1

zip -r visual_embeddings_$2.zip visual_embeddings_$2/
zip -r textual_embeddings_$2.zip textual_embeddings_$2/


mv visual_embeddings_$2.zip /home/matteo/Formal-Multimod-Rec/data/$1
mv textual_embeddings_$2.zip /home/matteo/Formal-Multimod-Rec/data/$1

cd /home/matteo/Formal-Multimod-Rec/data/$1
unzip visual_embeddings_$2.zip
unzip textual_embeddings_$2.zip


CUBLAS_WORKSPACE_CONFIG=:16:8 python3 mapping_copy.py --batch_size $2

cd /home/matteo/Formal-Multimod-Rec/

CUBLAS_WORKSPACE_CONFIG=:16:8 PYTHONPATH=. nohup python3 run_benchmarking.py --setting 4 --dataset $1 --batch_size $2 > ./ducho_logs/$1_logs/run_4_$2.txt &
CUBLAS_WORKSPACE_CONFIG=:16:8 PYTHONPATH=. nohup python3 run_benchmarking.py --setting 5 --dataset $1 --batch_size $2 > ./ducho_logs/$1_logs/run_5_$2.txt &

wait

cat ./ducho_logs/$1_logs/run_4_$2.txt | grep "Best Model results" > ./ducho_logs/$1_logs/run_4_$2_clean.txt
cat ./ducho_logs/$1_logs/run_5_$2.txt | grep "Best Model results" > ./ducho_logs/$1_logs/run_5_$2_clean.txt

scp ./ducho_logs/$1_logs/run_4_$2_clean.txt sisinflab@10.74.0.171:/share/Public/matteo/results/$1/
scp ./ducho_logs/$1_logs/run_5_$2_clean.txt sisinflab@10.74.0.171:/share/Public/matteo/results/$1/


# rm /home/matteo/Formal-Multimod-Rec/data/$1/visual_embeddings_$2.zip
# rm /home/matteo/Formal-Multimod-Rec/data/$1/textual_embeddings_$2.zip
# rm -rf /home/matteo/Formal-Multimod-Rec/data/$1/visual_embeddings_$2/
# rm -rf /home/matteo/Formal-Multimod-Rec/data/$1/textual_embeddings_$2/
# rm -rf /home/matteo/Formal-Multimod-Rec/data/$1/visual_embeddings_indexed_$2/
# rm -rf /home/matteo/Formal-Multimod-Rec/data/$1/textual_embeddings_indexed_$2/  
# rm -rf /home/matteo/Formal-Multimod-Rec/data/$1/train_indexed.tsv
# rm -rf /home/matteo/Formal-Multimod-Rec/data/$1/val_indexed.tsv  
# rm -rf /home/matteo/Formal-Multimod-Rec/data/$1/test_indexed.tsv  
# rm nohup.out 
# rm ./ducho_logs/$1_logs/run_4_$2.txt
# rm ./ducho_logs/$1_logs/run_5_$2.txt
