#!/bin/bash
#conda activate  /Users/chufang/opt/anaconda3/envs/GLAMOR_AAP
python dataWithSQLite.py 8888 &
# Likely only ports 22010-22020 (or some ports close to them) are open to public.
npm run serve -- --port $1 # 22011