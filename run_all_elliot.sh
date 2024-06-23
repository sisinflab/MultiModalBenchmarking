#!/bin/bash

python3 config_templates_elliot.py --dataset $1 --batch_size $2 --model $3

if [ ! -d ./ducho_logs ]; then
  mkdir ./ducho_logs
fi

if [ ! -d ./ducho_logs/$1_logs ]; then
  mkdir ./ducho_logs/$1_logs
fi

CUBLAS_WORKSPACE_CONFIG=:16:8 PYTHONPATH=. nohup python3 run_benchmarking.py --setting 1 --model $3 --dataset $1 --batch_size $2 > ./ducho_logs/$1_logs/run_1_$2_$3.txt &
CUBLAS_WORKSPACE_CONFIG=:16:8 PYTHONPATH=. nohup python3 run_benchmarking.py --setting 2 --model $3 --dataset $1 --batch_size $2 > ./ducho_logs/$1_logs/run_2_$2_$3.txt &
CUBLAS_WORKSPACE_CONFIG=:16:8 PYTHONPATH=. nohup python3 run_benchmarking.py --setting 3 --model $3 --dataset $1 --batch_size $2 > ./ducho_logs/$1_logs/run_3_$2_$3.txt &
CUBLAS_WORKSPACE_CONFIG=:16:8 PYTHONPATH=. nohup python3 run_benchmarking.py --setting 4 --model $3 --dataset $1 --batch_size $2 > ./ducho_logs/$1_logs/run_4_$2_$3.txt &
CUBLAS_WORKSPACE_CONFIG=:16:8 PYTHONPATH=. nohup python3 run_benchmarking.py --setting 5 --model $3 --dataset $1 --batch_size $2 > ./ducho_logs/$1_logs/run_5_$2_$3.txt &


wait

cat ./ducho_logs/$1_logs/run_1_$2_$3.txt | grep "Best Model results" > ./ducho_logs/$1_logs/run_1_$2_$3_clean.txt
cat ./ducho_logs/$1_logs/run_2_$2_$3.txt | grep "Best Model results" > ./ducho_logs/$1_logs/run_2_$2_$3_clean.txt
cat ./ducho_logs/$1_logs/run_3_$2_$3.txt | grep "Best Model results" > ./ducho_logs/$1_logs/run_3_$2_$3_clean.txt
cat ./ducho_logs/$1_logs/run_4_$2_$3.txt | grep "Best Model results" > ./ducho_logs/$1_logs/run_4_$2_$3_clean.txt
cat ./ducho_logs/$1_logs/run_5_$2_$3.txt | grep "Best Model results" > ./ducho_logs/$1_logs/run_5_$2_$3_clean.txt