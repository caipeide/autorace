#!/usr/bin/env python3

import os
import glob
import random
import json
import time
import zlib
from os.path import basename, join, splitext, dirname
import pickle
import datetime
import shutil

import numpy as np
from PIL import Image

import donkeycar as dk
from donkeycar.parts.datastore import Tub
from donkeycar.parts.augment import augment_image
from donkeycar.utils import *

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
from ai_drive_models import LinearModel, RNNModel, LinearResModel
from torch.utils.tensorboard import SummaryWriter
import matplotlib.pyplot as plt


def make_key(sample):
    tub_path = sample['tub_path']
    index = sample['index']
    return tub_path + str(index)


def make_next_key(sample, index_offset):
    tub_path = sample['tub_path']
    index = sample['index'] + index_offset
    return tub_path + str(index)


def collate_records(records, gen_records):
    '''
    open all the .json records from records list passed in,
    read their contents,
    add them to a list of gen_records, passed in.
    use the opts dict to specify config choices
    '''

    new_records = {}
    
    for record_path in records:

        basepath = os.path.dirname(record_path)        
        index = get_record_index(record_path)
        sample = { 'tub_path' : basepath, "index" : index }
             
        key = make_key(sample)

        if key in gen_records:
            continue

        try:
            with open(record_path, 'r') as fp:
                json_data = json.load(fp)
        except:
            continue

        image_filename = json_data["cam/image_array"]
        image_path = os.path.join(basepath, image_filename)

        # sample['record_path'] = record_path
        sample["image_path"] = image_path
        # sample["json_data"] = json_data        

        angle = float(json_data['user/angle'])
        throttle = float(json_data["user/throttle"])

        sample['angle'] = angle
        sample['throttle'] = throttle

        # # Initialise 'train' to False
        # sample['train'] = False
        
        # We need to maintain the correct train - validate ratio across the dataset, even if continous training
        # so don't add this sample to the main records list (gen_records) yet.
        new_records[key] = sample

    # Finally add all the new records to the existing list
    gen_records.update(new_records)
   
class EarlyStopping:
    # ref: https://github.com/Bjarten/early-stopping-pytorch
    """Early stops the training if validation loss doesn't improve after a given patience."""
    def __init__(self, patience=7, verbose=False, delta=0, path='checkpoint.pth', trace_func=print):
        """
        Args:
            patience (int): How long to wait after last time validation loss improved.
                            Default: 7
            verbose (bool): If True, prints a message for each validation loss improvement. 
                            Default: False
            delta (float): Minimum change in the monitored quantity to qualify as an improvement.
                            Default: 0
            path (str): Path for the checkpoint to be saved to.
                            Default: 'checkpoint.pt'
            trace_func (function): trace print function.
                            Default: print            
        """
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.Inf
        self.delta = delta
        self.path = path
        self.trace_func = trace_func
    def __call__(self, val_loss, model):

        score = -val_loss

        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
        elif score < self.best_score + self.delta:
            self.counter += 1
            self.trace_func(f'EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
            self.counter = 0
    def save_checkpoint(self, val_loss, model):
        '''Saves model when validation loss decrease.'''
        if self.verbose:
            self.trace_func(f'Validation loss decreased ({self.val_loss_min:.6f} --> {val_loss:.6f}).  Saving model ...')
        torch.save(model.state_dict(), self.path)
        self.val_loss_min = val_loss


def start_train(cfg, tub_names, model_path, model_type, pretrain_path, sequence_train = False):
    # ref: https://github.com/Bjarten/early-stopping-pytorch/blob/master/MNIST_Early_Stopping_example.ipynb
    '''
    use the specified data in tub_names to train an artifical neural network
    saves the output trained model as model_name
    ''' 
    
    if model_type is None:
        model_type = cfg.DEFAULT_MODEL_TYPE

    print('training with model type', model_type)

    # --------------------------
    # 1. dataset
    # --------------------------
    records = gather_records(cfg, tub_names, verbose=True) # json in tubs
    
    print('collating %d records ...' % (len(records)))
    gen_records = {}
    collate_records(records, gen_records)

    if not sequence_train:
        
        from DataLoader import load_split_train_valid
        trainloader, validloader = load_split_train_valid(cfg, gen_records, num_workers=cfg.NUM_WORKERS)
        print(len(trainloader), len(validloader))
    else:
        print('collating sequences based on the records ...')

        sequences = []
        
        target_len = cfg.SEQUENCE_LENGTH

        for k, sample in gen_records.items():

            seq = []

            for i in range(target_len):
                key = make_next_key(sample, i)
                if key in gen_records:
                    seq.append(gen_records[key]) # list_3_dict
                else:
                    continue

            if len(seq) != target_len:
                continue

            sequences.append(seq) # list_list_3_dict

        print("collated", len(sequences), "sequences of length", target_len)

        #shuffle and split the data
        train_data_list = []
        target_train_size = len(sequences) * cfg.TRAIN_TEST_SPLIT

        i_sample = 0

        while i_sample < target_train_size and len(sequences) > 1:
            i_choice = random.randint(0, len(sequences) - 1)
            train_data_list.append(sequences.pop(i_choice))
            i_sample += 1

        # remainder of the original list is the validation set
        val_data_list = sequences
        from DataLoader_sequence import load_split_train_valid
        trainloader, validloader = load_split_train_valid(cfg, train_data_list, val_data_list, num_workers=cfg.NUM_WORKERS)
        print(len(trainloader), len(validloader))

    if len(trainloader) < 2:
        raise Exception("Too little data to train. Please record more records.")


    # --------------------------
    # 2. model
    # --------------------------
    device = torch.device('cuda')
    if model_type == 'linear':
        drive_model = LinearModel()
        print('linear model created')
    elif model_type == 'resnet18':
        drive_model = LinearResModel()
        print('resnet18 model created')
    elif model_type == 'rnn':
        drive_model = RNNModel()
        print('rnn model created')
    # load the pre-trained model if specified
    if pretrain_path:
        print('loading the pretrained model from path: ', pretrain_path)
        t0 = time.time()
        drive_model.load_state_dict(torch.load(pretrain_path,map_location=lambda storage, loc: storage))
        print('pretrained model loaded, time cost: %.5f s'%(time.time()-t0))
    drive_model = drive_model.to(device)
    path_tensorboard = os.path.dirname(model_path) + '/' + os.path.basename(model_path).split('.')[0]
    if os.path.exists(path_tensorboard):
        shutil.rmtree(path_tensorboard)
    writer = SummaryWriter(path_tensorboard)
    # early stopping patience; how long to wait after last time validation loss improved.
    patience = cfg.EARLY_STOP_PATIENCE
    params = drive_model.parameters()
    optimizer = torch.optim.Adam(params, lr=cfg.LEARNING_RATE)


    # --------------------------
    # 3. start to train
    # --------------------------
    if cfg.PRINT_MODEL_SUMMARY:
        print(drive_model)
    drive_model, train_loss, valid_loss = go_train(trainloader, validloader, device, optimizer, drive_model, writer, patience, cfg, model_path)
    

    # --------------------------
    # 4. plot the curve
    # --------------------------
    # visualize the loss as the network trained
    fig = plt.figure(figsize=(10,8))
    plt.plot(range(1,len(train_loss)+1),train_loss, label='Training Loss')
    plt.plot(range(1,len(valid_loss)+1),valid_loss,label='Validation Loss')

    # find position of lowest validation loss
    minposs = valid_loss.index(min(valid_loss))+1 
    plt.axvline(minposs, linestyle='--', color='r',label='Early Stopping Checkpoint')

    plt.xlabel('epochs')
    plt.ylabel('loss')
    # plt.ylim(0, 0.5) # consistent scale
    plt.xlim(0, len(train_loss)+1) # consistent scale
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    fig.savefig(os.path.dirname(model_path) + '/loss_plot_' + os.path.basename(model_path).split('.')[0] + '.png', bbox_inches='tight')

def go_train(trainloader, validloader, device, optimizer, drive_model, writer, patience, cfg, model_path):
    # to track the training loss as the model trains
    train_losses = []
    # to track the validation loss as the model trains
    valid_losses = []
    # to track the average training loss per epoch as the model trains
    avg_train_losses = []
    # to track the average validation loss per epoch as the model trains
    avg_valid_losses = [] 
    
    # initialize the early_stopping object
    early_stopping = EarlyStopping(patience=patience, verbose=True, path=model_path, delta=cfg.MIN_DELTA)

    start_epoch = 1
    for epoch in range(start_epoch, 1 + cfg.MAX_EPOCHS):
        drive_model.train()

        for i, sample_batch in enumerate(trainloader):
            rgb = sample_batch['rgb'].to(device)
            steering = sample_batch['steering'].to(device)
            throttle = sample_batch['throttle'].to(device)

            optimizer.zero_grad()

            net_steering, net_throttle = drive_model(rgb)

            loss_steer = F.mse_loss(net_steering, steering)
            loss_throttle = F.mse_loss(net_throttle, throttle)
            loss = loss_steer + loss_throttle
            loss.backward()
            optimizer.step()

            writer.add_scalar('Train/Loss_steer', loss_steer.item(), len(trainloader)*(epoch-1) + i+1 )
            writer.add_scalar('Train/Loss_throttle', loss_throttle.item(), len(trainloader)*(epoch-1) + i+1 )
            writer.add_scalar('Train/Loss', loss.item(), len(trainloader)*(epoch-1) + i+1 )

            print('Epoch: {}, [Batch: {}/ TotalBatch: {}] Train_BatchLoss: {:.3f}'.format(epoch, i+1 , len(trainloader), loss.item()),end='\r')

            train_losses.append(loss.item())
        
        print()
        drive_model.eval()
        valid_losses_steer = []
        valid_losses_throttle = []

        with torch.no_grad():
            for i, sample_batch in enumerate(validloader):
                rgb = sample_batch['rgb'].to(device)
                steering = sample_batch['steering'].to(device)
                throttle = sample_batch['throttle'].to(device)

                net_steering, net_throttle = drive_model(rgb)

                loss_steer = F.mse_loss(net_steering, steering)
                loss_throttle = F.mse_loss(net_throttle, throttle)
                loss = loss_steer + loss_throttle

                valid_losses.append(loss.item())
                valid_losses_steer.append(loss_steer.item())
                valid_losses_throttle.append(loss_throttle.item())

                print('Epoch: {} [Batch: {}/ TotalBatch: {}] Valid_BatchLoss: {:.3f}'.format(epoch, i+1 , len(validloader), loss.item()),end='\r')

        writer.add_scalar('Valid/Loss_steer', np.average(valid_losses_steer), epoch)
        writer.add_scalar('Valid/Loss_throttle', np.average(valid_losses_throttle), epoch)
        writer.add_scalar('Valid/Loss', np.average(valid_losses), epoch)

        # print training/validation statistics 
        # calculate average loss over an epoch
        train_loss = np.average(train_losses)
        valid_loss = np.average(valid_losses)
        avg_train_losses.append(train_loss)
        avg_valid_losses.append(valid_loss)

        epoch_len = len(str(cfg.MAX_EPOCHS))

        print_msg = (f'[{epoch:>{epoch_len}}/{cfg.MAX_EPOCHS:>{epoch_len}}] ' + 
                    f'train_loss: {train_loss:.5f} ' +
                    f'valid_loss: {valid_loss:.5f}')
        print()
        print(print_msg)
        
        # clear lists to track next epoch
        train_losses = []
        valid_losses = []

        # early_stopping needs the validation loss to check if it has decresed, 
        # and if it has, it will make a checkpoint of the current model
        early_stopping(valid_loss, drive_model)
        print()
        
        if early_stopping.early_stop:
            print("Early stopping")
            break

    return drive_model, avg_train_losses, avg_valid_losses

def multi_train(cfg, tub, model, model_type, pretrain_path):
    '''
    choose the right regime for the given model type
    '''
    sequence_train = False
    if model_type in ("rnn",'3d','look_ahead'):
        sequence_train = True

    start_train(cfg, tub, model, model_type, pretrain_path, sequence_train = sequence_train)

    
def removeComments( dir_list ):
    for i in reversed(range(len(dir_list))):
        if dir_list[i].startswith("#"):
            del dir_list[i]
        elif len(dir_list[i]) == 0:
            del dir_list[i]

def preprocessFileList( filelist ):
    dirs = []
    if filelist is not None:
        for afile in filelist:
            with open(afile, "r") as f:
                tmp_dirs = f.read().split('\n')
                dirs.extend(tmp_dirs)

    removeComments( dirs )
    return dirs