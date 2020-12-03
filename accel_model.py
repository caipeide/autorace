#!/usr/bin/env python3
"""
Scripts to accelerate a normal pytorch model

Usage:
    accel_model.py (--model=<model>) [--half] (--type=<>) [--myconfig=<filename>]

Options:
    -h --help                  Show this screen.
    --half                     Use half pression, which will take less memory during inference
    --myconfig=filename        Specify myconfig file to use. 
                               [default: myconfig.py]
"""
import torch
from ai_drive_models import LinearModel, RNNModel, LinearResModel
from torch2trt import torch2trt
from docopt import docopt
import os
import time
import donkeycar as dk

def accel_torch_model(cfg, model_type, model_path = './', use_half = False):
    
    # load the original model
    device = torch.device('cuda')
    if model_type == 'linear' or model_type == 'resnet18':
        if model_type == 'linear':
            drive_model = LinearModel().to(device)
        elif model_type == 'resnet18':
            drive_model = LinearResModel().to(device)
        data = torch.zeros((1, 3, 224, 224)).cuda()
    elif model_type == 'rnn':
        drive_model = RNNModel().to(device)
        seq_length = cfg.SEQUENCE_LENGTH
        data = torch.zeros((1, seq_length, 3, 224, 224)).cuda()
    
    drive_model.eval()
    if use_half:
        drive_model.half()
        data = data.half()

    drive_model.load_state_dict(torch.load(model_path,map_location=lambda storage, loc: storage))
    # start to compress
    model_trt = torch2trt(drive_model, [data], fp16_mode=use_half)
    if use_half:
        new_path = os.path.join(os.path.dirname(model_path), os.path.basename(model_path).split('.')[0]+'_trt_half.pth')
    else:
        new_path = os.path.join(os.path.dirname(model_path), os.path.basename(model_path).split('.')[0]+'_trt.pth')
    torch.save(model_trt.state_dict(), new_path)
    print('saving the accelerateed model to: ', new_path)


if __name__ == '__main__':
    args = docopt(__doc__)
    cfg = dk.load_config(myconfig=args['--myconfig'])

    model_path = args['--model']
    use_half = args['--half']
    model_type = args['--type']
    print('start to accel the model: ', model_path, ' | using half pression: ', use_half)
    time_start = time.time()
    accel_torch_model(cfg, model_type, model_path = model_path, use_half=use_half)
    print('acceleration finished :) time cost: %.2f s'%(time.time() - time_start))
