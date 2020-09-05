#!/bin/sh
python detect.py --weights ./weights/box_weight.pt  --img 416 --conf 0.5 --source 0  --device 'cpu'