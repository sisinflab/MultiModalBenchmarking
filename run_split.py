import os
import shutil
from elliot.run import run_experiment

if not (os.path.exists('./data/baby/train.tsv') and os.path.exists('./data/baby/val.tsv') and os.path.exists('./data/baby/test.tsv')):
    run_experiment(f"config_files/split.yml")
    shutil.move('./data/baby_splits/0/test.tsv', './data/baby/test.tsv')
    shutil.move('./data/baby_splits/0/0/train.tsv', './data/baby/train.tsv')
    shutil.move('./data/baby_splits/0/0/val.tsv', './data/baby/val.tsv')
    shutil.rmtree('./data/baby_splits/')

if not (os.path.exists('./data/music/train.tsv') and os.path.exists('./data/music/val.tsv') and os.path.exists('./data/music/test.tsv')):
    run_experiment(f"config_files/split.yml")
    shutil.move('./data/music_splits/0/test.tsv', './data/music/test.tsv')
    shutil.move('./data/music_splits/0/0/train.tsv', './data/music/train.tsv')
    shutil.move('./data/music_splits/0/0/val.tsv', './data/music/val.tsv')
    shutil.rmtree('./data/music_splits/')

if not (os.path.exists('./data/office/train.tsv') and os.path.exists('./data/office/val.tsv') and os.path.exists('./data/office/test.tsv')):
    run_experiment(f"config_files/split.yml")
    shutil.move('./data/office_splits/0/test.tsv', './data/office/test.tsv')
    shutil.move('./data/office_splits/0/0/train.tsv', './data/office/train.tsv')
    shutil.move('./data/office_splits/0/0/val.tsv', './data/office/val.tsv')
    shutil.rmtree('./data/office_splits/')