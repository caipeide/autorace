<div align=center>
<img src=images/logo.png width="65%">

![license](https://img.shields.io/github/license/caipeide/autorace)
![code_size](https://img.shields.io/github/languages/code-size/caipeide/autorace)
![total_Lines](https://img.shields.io/tokei/lines/github/caipeide/autorace)
![last_update](https://img.shields.io/github/last-commit/caipeide/autorace)
![stars](https://img.shields.io/github/stars/caipeide/autorace?style=social)
</div>

<div align=center>
<img src=images/demo.gif width="70%">
</div>

Autorace provides hardware components and example codes to achieve vision-based autonomous racing on RC-Cars. It is developed by [RAM-LAB](https://www.ram-lab.com/) to support *the 1st autonomous RC-Car racing competition* in Hong Kong University of Science and Technology (HKUST). The competition data is Feb 26, 2021 (tentative).

**Event Collaborators**: School of Engineering, Robotics Institue (RI), Robotics and Multiperception Lab (RAM-LAB), Intelligent Autonomous Driving Center, Entrepreneurship Center

**Keywords:** autonomous racing, visual navigation, artifical intelligence, deep learning.

**Maintaners:** [Peide Cai](https://www.ram-lab.com/people/#mr-peide-cai) &lt;pcaiaa@connect.ust.hk&gt;

💻 [Official Website](https://ecenter.ust.hk/events/hkust-autonomous-rc-car-racing-competition)

📹 [Demo & Workshops](https://sites.google.com/view/autorc-racing/)

🏁 [Rules and Regulations](https://www.ec.ust.hk/sites/default/files/1/HKUST%20Autonomous%20RC-car%20Racing%20Competition_1.pdf)




# Table of Contents <!-- omit in toc -->
- [Featuress](#featuress)
- [Build a RC-Car](#build-a-rc-car)
- [System Installation](#system-installation)
  - [Jetson Nano on the RC-Car](#jetson-nano-on-the-rc-car)
  - [Your Host PC](#your-host-pc)
    - [Server usage](#server-usage)
- [Train a Self-driving Car](#train-a-self-driving-car)
  - [Data Collection](#data-collection)
  - [Model Training](#model-training)
    - [Accelerate your model](#accelerate-your-model)
  - [Model Testing](#model-testing)
- [Notes](#notes)
- [Other Useful Toturials](#other-useful-toturials)
  - [PyTorch](#pytorch)
  - [Python3](#python3)
  - [Deep Learning](#deep-learning)
  - [Jetson Nano](#jetson-nano)
- [Credits](#credits)
  
## Featuress
* Coding language: *Python3*
* Deep learning framework: [*PyTorch 1.6*](https://pytorch.org/)
* On-board computer: [*Jetson Nano B1*](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-nano/)
* Complete pipeline of data collection, model training and testing
* Easy to use and DIY
* What can you achieve 🤔?

    1. Build a small but powerful RC-Car that can drive itself.
    2. Record driving data (camera images, control actions) by teleoperating the RC-Car.
    3. Train different AI autopilots to drive your car on the track as fast as possible.
    4. Autonomous collision avoidance around different obstacles.

## Build a RC-Car
<div align=center>
<img src=images/car.jpg width="60%">
</div>

The RC-Car is named JetRacer, a high speed AI racing robot powered by Jetson Nano.

Website: [中文](https://www.waveshare.net/shop/JetRacer-Pro-AI-Kit.htm) | [EN](https://www.waveshare.com/product/ai/robots/mobile-robots/jetracer-pro-ai-kit.htm) 

JetRacer WiKi: [中文](https://www.waveshare.net/wiki/JetRacer_Pro_AI_Kit) | [EN](https://www.waveshare.com/wiki/JetRacer_Pro_AI_Kit)

> Some parts of the user guides on software in the above wiki (provided by the vendor) are out-of-date (you may meet different errors during tests). Please follow this repository for system and software installation in the following sections, and just take the above wiki as a reference.

Assemble Manusal: [中文](images/Jetracer_pro_Assembly_CN.pdf) | [EN](images/Jetracer_pro_Assembly_EN.pdf) 

Slides and Assemble Video: [Link](https://sites.google.com/view/autorc-racing/workshops#h.2vgfpvidyayt)


## System Installation

### Jetson Nano on the RC-Car 
*This is for data collection and model deployment*

### Your Host PC
*This is for AI model training*


*For the participants who do not have a NVIDIA graphics card (GPU) in their computer, they can apply for using a server to train their models.*
#### Server usage

```console
$ ssh -p 1234 team1@xx.xx.xx.xx
```

## Train a Self-driving Car

### Data Collection
Randomly place different obstacles on the track.

```console
$ python manage.py drive --js
```

### Model Training
```console
$ python manage.py train --model models/resnet18.pth --type resnet18
```

#### Accelerate your model
```console
$ python accel_model.py --model models/resnet18.pth --half --type resnet18
```
### Model Testing
```console
$ python manage.py drive --model models/resnet18_trt.pth --half --trt --type resnet18
```

## Notes

1. Remember to configure the system on Jetson Nano to 5W mode to increase battery life (default: MAXN) `sudo nvpmodel -m1`
2. Do not directly turn off the power when system is running. Open a terminal and do`sudo shutdown`first to shutdown the OS system, then turn off the power.
3. If the RC-Car crashes into the track fence at a high speed, the front wheels are likely to get stuck at their drive rods. Then you need to remove the two drive rods and reinstall them, which is a little troublesome. *It is suggested to simply remove the drive rod of the two front wheels, then this problem can be solved.*

## Other Useful Toturials

### PyTorch
- https://github.com/MorvanZhou/PyTorch-Tutorial
- https://github.com/yunjey/pytorch-tutorial
- https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html

### Python3

### Deep Learning

### Jetson Nano


## Credits
* [Donkeycar](https://github.com/autorope/donkeycar): Open source hardware and software platform to build a small scale self driving car.
* [JetRacer](https://github.com/NVIDIA-AI-IOT/jetracer): An autonomous AI racecar using NVIDIA Jetson Nano.
* [Jetcard](https://github.com/NVIDIA-AI-IOT/jetcard): An SD card image for web programming AI projects with NVIDIA Jetson Nano.
* [torch2trt](https://github.com/NVIDIA-AI-IOT/torch2trt): An easy to use PyTorch to TensorRT converter for model acceleration. Real-time computing performance is important for our high-speed driving occasions.