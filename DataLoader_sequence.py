from PIL import Image
import os
import torch
import torch.utils.data
import pandas
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import csv
import json
import math
import random

seed = 123

class SelfDriveDataset(Dataset):

    def __init__(self, dataset_list_list_dicts, transform = None):
        self.dataset_list_list_dicts = dataset_list_list_dicts
        self.transform = transform
        
    def __len__(self): 
        return len(self.dataset_list_list_dicts)

    def __getitem__(self, idx):
        this_data = self.dataset_list_list_dicts[idx]

        rgbs = []

        for d in this_data: # this_data is a list of cfg.SEQUENCE_LENGTH dicts, each dict is a record of one-frame data.
            rgb_path = d['image_path']
            rgb = Image.open(rgb_path)
            if self.transform is not None: # add noise to the dataset...just for training... 
                rgb = self.transform(rgb)
            rgbs.append(rgb)
        
        rgbs = torch.stack( [transforms.ToTensor()(rgbs[k]) for k in range(len(rgbs))], dim=0 )
        
        future_steer = np.array(this_data[-1]['angle'])
        future_throttle = np.array(this_data[-1]['throttle'])

        sample = {'rgb': rgbs, 
                'steering': torch.from_numpy(future_steer).float(),
                'throttle': torch.from_numpy(future_throttle).float()}

        return sample

    
def load_split_train_valid(cfg, train_data_list_list_dicts, val_data_list_list_dicts, num_workers=2):

    batch_size = cfg.BATCH_SIZE
    
    if cfg.COLOR_JITTER_TRANSFORMS:
        train_transforms = transforms.Compose([transforms.ColorJitter(brightness=0.5, contrast=0.3, saturation=0.3, hue=0.3)])  # add image noise later...
        print('using COLOR_JITTER_TRANSFORMS during training...')   
    else:
        train_transforms = None

    train_data = SelfDriveDataset(train_data_list_list_dicts,transform=train_transforms)
    valid_data = SelfDriveDataset(val_data_list_list_dicts,transform=None)

    trainloader = DataLoader(train_data, batch_size=batch_size, num_workers=num_workers, shuffle=True)
    validloader = DataLoader(valid_data, batch_size=batch_size, num_workers=num_workers, shuffle=True)
    
    return trainloader, validloader