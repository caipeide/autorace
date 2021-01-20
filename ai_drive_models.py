import time
import torch
import torchvision
from PIL import Image
import torch.nn as nn
import cv2
from torchvision.models import resnet18
import numpy as np
from torchvision import transforms

class DriveClass:
    # used for inference, with the ai-drive-model packed.
    def __init__(self, cfg, model_type, drive_model, device, cam = None, half = False):

        self.drive_model = drive_model
        self.run_steering = 0.0
        self.run_throttle = 0.0
        self.cam = cam
        self.device = device
        self.half = half
        self.model_type = model_type
        self.img_seq = []
        self.seq_length = cfg.SEQUENCE_LENGTH
        # initialize the deep network model, the first inference time is a bit slow
        print('waiting for the camera image to warm up the network.')
        while True:
            img_arr = self.cam.run() # cv2, numpy array
            time.sleep(0.5)
            if img_arr is not None:
                break 
        print('warming up the deep network model...')
        t0 = time.time()
        # self.run(np.ones([cfg.IMAGE_H, cfg.IMAGE_W, cfg.IMAGE_DEPTH]).astype(np.uint8)*255)
        self.run(img_arr)
        print('network initialized, time cost: %.2f s'%(time.time()-t0))
        

    def update(self):
        while self.cam.running:
            # read the memory and compute
            img_arr = self.cam.run_threaded() # cv2, numpy array
            if img_arr is None:
                continue
            
            if self.model_type == 'linear' or self.model_type == 'resnet18':
                # print(img_arr.shape) # 224, 224, 3
                img_arr = Image.fromarray(img_arr)
                if self.half:
                    img_arr = transforms.ToTensor()(img_arr).half()
                else:
                    img_arr = transforms.ToTensor()(img_arr)
                img_arr = torch.unsqueeze(img_arr, 0).to(self.device)
                run_steering, run_throttle = self.drive_model(img_arr)
            elif self.model_type == 'rnn':
                while len(self.img_seq) < self.seq_length:
                    self.img_seq.append(Image.fromarray(img_arr))

                self.img_seq = self.img_seq[1:]
                self.img_seq.append(Image.fromarray(img_arr))
                
                rgbs = torch.stack( [transforms.ToTensor()(self.img_seq[k]) for k in range(self.seq_length)], dim=0 )
                if self.half:
                    rgbs = rgbs.half()
                rgbs = torch.unsqueeze(rgbs, 0).to(self.device)
                run_steering, run_throttle = self.drive_model(rgbs)
            
            
            run_steering = float(run_steering.detach().cpu().numpy())
            run_throttle = float(run_throttle.detach().cpu().numpy())

            self.run_steering = run_steering
            self.run_throttle = run_throttle
            
    def run(self, img_arr):
        if self.model_type == 'linear' or self.model_type == 'resnet18':
            # print(img_arr.shape) # 224, 224, 3
            img_arr = Image.fromarray(img_arr)
            if self.half:
                img_arr = transforms.ToTensor()(img_arr).half()
            else:
                img_arr = transforms.ToTensor()(img_arr)
            img_arr = torch.unsqueeze(img_arr, 0).to(self.device)
            run_steering, run_throttle = self.drive_model(img_arr)
        elif self.model_type == 'rnn':
            while len(self.img_seq) < self.seq_length:
                self.img_seq.append(Image.fromarray(img_arr))

            self.img_seq = self.img_seq[1:]
            self.img_seq.append(Image.fromarray(img_arr))
            
            rgbs = torch.stack( [transforms.ToTensor()(self.img_seq[k]) for k in range(self.seq_length)], dim=0 )
            if self.half:
                rgbs = rgbs.half()
            rgbs = torch.unsqueeze(rgbs, 0).to(self.device)
            run_steering, run_throttle = self.drive_model(rgbs)
           
        
        run_steering = float(run_steering.detach().cpu().numpy())
        run_throttle = float(run_throttle.detach().cpu().numpy())
        return run_steering, run_throttle
    
    def run_threaded(self, img_arr):
        return self.run_steering, self.run_throttle


class LinearModel(nn.Module):
    def __init__(self):
        super(LinearModel, self).__init__()
        # similar to the self-driving car model from Nvidia in 2016: https://developer.nvidia.com/blog/deep-learning-self-driving-cars/
        self.layer_cnn = nn.Sequential(
            nn.Conv2d(in_channels= 3, out_channels= 32, kernel_size=3, stride=2, padding=1), #size: 224-->112
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels= 32, out_channels= 64, kernel_size=3, stride=2, padding=1), #112-->56
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels= 64, out_channels= 128, kernel_size=3, stride=2, padding=1), #56-->28
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels= 128, out_channels= 256, kernel_size=3, stride=2, padding=1), #28-->14
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels= 256, out_channels= 512, kernel_size=3, stride=2, padding=1), #14-->7, final size: batch_size*512*7*7
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True)
        )
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1)) # pooling, change the size to batch_size*512*1*1

        self.layer_steering = nn.Sequential(
                            nn.Linear(512, 256), nn.BatchNorm1d(256), nn.ReLU(True),
                            nn.Linear(256, 128), nn.BatchNorm1d(128), nn.ReLU(True),
                            nn.Linear(128, 1)
        )

        self.layer_throttle = nn.Sequential(
                            nn.Linear(512, 256), nn.BatchNorm1d(256), nn.ReLU(True),
                            nn.Linear(256, 128), nn.BatchNorm1d(128), nn.ReLU(True),
                            nn.Linear(128, 1)
        )

    def forward(self, rgb):
        x = self.layer_cnn(rgb) # batch, 512, 7,7
        x = self.avgpool(x) # batch, 512, 1, 1
        x = torch.flatten(x, start_dim=1) # flatten to size of: batch_size*512

        steering = self.layer_steering(x)
        throttle = self.layer_throttle(x)

        return steering[:,0], throttle[:,0]


class LinearResModel(nn.Module):
    def __init__(self):
        super(LinearResModel, self).__init__()
        self.resnet_rgb = resnet18(pretrained=False)
        self.resnet_rgb.fc = nn.Sequential(
                            nn.Linear(512, 512), nn.BatchNorm1d(512), nn.ReLU(True))
        self.layer_steering = nn.Sequential(
                            nn.Linear(512, 256), nn.BatchNorm1d(256), nn.ReLU(True),
                            nn.Linear(256, 128), nn.BatchNorm1d(128), nn.ReLU(True),
                            nn.Linear(128, 1)
        )

        self.layer_throttle = nn.Sequential(
                            nn.Linear(512, 256), nn.BatchNorm1d(256), nn.ReLU(True),
                            nn.Linear(256, 128), nn.BatchNorm1d(128), nn.ReLU(True),
                            nn.Linear(128, 1)
        )

    def forward(self, rgb):
        x = self.resnet_rgb(rgb)

        steering = self.layer_steering(x)
        throttle = self.layer_throttle(x)

        return steering[:,0], throttle[:,0]


class RNNModel(nn.Module):
    def __init__(self):
        super(RNNModel, self).__init__()

        self.resnet_rgb = resnet18(pretrained=False)
        
        self.resnet_rgb.fc = nn.Sequential(
                            nn.Linear(512, 512), nn.BatchNorm1d(512), nn.ReLU(True))
        
        self.layer_steering = nn.Sequential(
                            nn.Linear(256, 256), nn.BatchNorm1d(256), nn.ReLU(True),
                            nn.Linear(256, 128), nn.BatchNorm1d(128), nn.ReLU(True),
                            nn.Linear(128, 1)
        )

        self.layer_throttle = nn.Sequential(
                            nn.Linear(256, 256), nn.BatchNorm1d(256), nn.ReLU(True),
                            nn.Linear(256, 128), nn.BatchNorm1d(128), nn.ReLU(True),
                            nn.Linear(128, 1)
        )

        self.layer_lstm = nn.LSTM(512, hidden_size=256, num_layers=3, batch_first=True)

    def forward(self, rgbs):
        batch_size_actual_val = rgbs.size(0)
        img_features = torch.Tensor(batch_size_actual_val,rgbs.size(1),512).cuda()
        for p in range(rgbs.size(1)):
            img_features[:,p,:] = self.resnet_rgb(rgbs[:,p,:,:,:]) # 2,12,3,224,224

        seq_features,_ = self.layer_lstm(img_features)

        seq_feature = seq_features[:,-1,:]

        steering = self.layer_steering(seq_feature)
        throttle = self.layer_throttle(seq_feature)

        return steering[:,0], throttle[:,0]

