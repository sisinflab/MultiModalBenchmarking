#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--gpu_id', type=int, default=0, help='choose the gpu id')
parser.add_argument('--mm_batch_size', type=int, default=1, help='choose the batch size for the multimodal extractor')
parser.add_argument('--datasets', type=str, nargs='+', default='office music baby', help='choose the datasets')
parser.add_argument('--cluster', type=str, default='', help='cluster name')
parser.add_argument('--mail_user', type=str, default='', help='your email')
parser.add_argument('--account', type=str, default='', help='project name')
parser.add_argument('--partition', type=str, default='', help='partition name')

args = parser.parse_args()


def main():
    datasets = args.datasets
    logs_path = 'logs'
    scripts_path = 'scripts'

    if not os.path.exists(logs_path):
        os.makedirs(logs_path)

    if not os.path.exists(scripts_path):
        os.makedirs(scripts_path)

    command_lines = list()

    for dataset in datasets:
        completed = False
        if os.path.isfile(f'{logs_path}/logfile_{dataset}_{args.mm_batch_size}.log'):
            with open(f'{logs_path}/logfile_{dataset}_{args.mm_batch_size}.log', 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                completed = ('Best Model params' in content) and ('queue.Full' not in content)

        if not completed:
            command_line = (f'CUBLAS_WORKSPACE_CONFIG=:4096:8 ./run_all_ducho.sh {dataset} {args.mm_batch_size} > {logs_path}/logfile_{dataset}_{args.mm_batch_size}.log 2>&1')
            command_lines += [command_line]

    header = None

    if args.cluster == 'cineca':
        header = """#!/bin/bash -l
#SBATCH --job-name=SisInfLab_Ducho_Elliot
#SBATCH --time=24:00:00                                   ## format: HH:MM:SS
#SBATCH --nodes=1
#SBATCH --mem=20GB                                       ## memory per node out of 494000MB (481GB)
#SBATCH --output=../../../slogs/SisInfLab_Ducho_Elliot_output-%A_%a.out
#SBATCH --error=../../../slogs/SisInfLab_Ducho_Elliot_error-%A_%a.err
#SBATCH --account={1}
#SBATCH --mail-type=ALL
#SBATCH --mail-user={2}
#SBATCH --gres=gpu:1                                    ##    1 out of 4 or 8
#SBATCH --partition=boost_usr_prod
#SBATCH --qos=normal
#SBATCH --array=1-{0}

source ~/.bashrc
set -x

module load gcc/12.2.0-cuda-12.1
module load python/3.10.8--gcc--11.3.0

cd $HOME/workspace/MultiModalBenchmarking

source venv/bin/activate

export LANG="en_US.utf8"
export LANGUAGE="en_US:en"

echo "Run experiments"
"""

    if header:
        with open(scripts_path + f'/' + f'{"_".join(args.datasets)}_{args.mm_batch_size}.sh', 'w') as f:
            print(header.format(len(datasets), args.account, args.mail_user), file=f)
            for idx, dataset in enumerate(datasets):
                current_command_line = command_lines[idx]
                print(f'{current_command_line}', file=f)
    else:
        with open(f'run_all_{"_".join(args.datasets)}.sh', 'w') as f:
            print(f'#!/bin/bash', file=f)
            for command_line in command_lines:
                print(f'{command_line}', file=f)


if __name__ == '__main__':
    main()
