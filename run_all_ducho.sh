#!/bin/bash

python3 config_templates_ducho.py --dataset $1 --batch_size $2

cd ./Ducho

PYTHONPATH=. python3 ./demos/demo_$1/run.py > ./ducho_log.txt

cd ..

cp -rf ./Ducho/local/data/demo_$1/visual_embeddings_$2 ./data/$1
cp -rf ./Ducho/local/data/demo_$1/textual_embeddings_$2 ./data/$1


cp ./Ducho/local/data/demo_$1/reviews.tsv ./data/$1
CUBLAS_WORKSPACE_CONFIG=:16:8 python3 run_split.py --dataset $1

cd ./data/$1
CUBLAS_WORKSPACE_CONFIG=:16:8 python3 mapping.py --batch_size $2