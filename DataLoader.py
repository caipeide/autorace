from PIL import Image
import os
import torch
import torch.utils.data
import pandas
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
from torch.utils.data.sampler import SubsetRandomSampler
import csv
import json
import math
import random

seed = 123

class SelfDriveDataset(Dataset):

    def __init__(self, dataset_list_dict, transform = None):
        self.dataset_list_dict = dataset_list_dict
        self.transform = transform
        
    def __len__(self): 
        return len(self.dataset_list_dict)

    def __getitem__(self, idx):
        this_data = self.dataset_list_dict[idx]
        
        future_steer = np.array(this_data['angle'])
        future_throttle = np.array(this_data['throttle'])

        rgb_path = this_data['image_path']
        rgb = Image.open(rgb_path)
        if self.transform is not None: # add noise to the dataset...just for training... 
            rgb = self.transform(rgb)
        rgb = transforms.ToTensor()(rgb)
        # TODO add transforms later...


        sample = {'rgb': rgb, 
                'steering': torch.from_numpy(future_steer).float(),
                'throttle': torch.from_numpy(future_throttle).float()}
        
        

        return sample

    
def load_split_train_valid(cfg, collate_records_dict_dict, num_workers=2):

    batch_size = cfg.BATCH_SIZE
    if cfg.COLOR_JITTER_TRANSFORMS:
        train_transforms = transforms.Compose([transforms.ColorJitter(brightness=0.5, contrast=0.3, saturation=0.3, hue=0.3)])  # add image noise later...
        print('using COLOR_JITTER_TRANSFORMS during training...')
    else:
        train_transforms = None

    # new_records now contains all our NEW samples
    # - set a random selection to be the training samples based on the ratio in CFG file
    train_data_list_dict = []
    valid_data_list_dict = []

    shufKeys = list(collate_records_dict_dict.keys())
    random.seed(seed)
    random.shuffle(shufKeys)
    trainCount = 0
    #  Ratio of samples to use as training data, the remaining are used for evaluation
    targetTrainCount = int(cfg.TRAIN_TEST_SPLIT * len(shufKeys))
    for key in shufKeys:
        if trainCount < targetTrainCount:
            train_data_list_dict.append(collate_records_dict_dict[key])
        trainCount += 1
        if trainCount >= targetTrainCount:
            valid_data_list_dict.append(collate_records_dict_dict[key])

    train_data = SelfDriveDataset(train_data_list_dict,transform=train_transforms)
    valid_data = SelfDriveDataset(valid_data_list_dict,transform=None)

    trainloader = DataLoader(train_data, batch_size=batch_size, num_workers=num_workers, shuffle=True)
    validloader = DataLoader(valid_data, batch_size=batch_size, num_workers=num_workers, shuffle=True)
    
    return trainloader, validloader