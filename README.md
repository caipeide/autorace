<div align=center>
<img src=images/logo.png width="65%">

![license](https://img.shields.io/github/license/caipeide/autorace)
![code_size](https://img.shields.io/github/languages/code-size/caipeide/autorace)
![total_Lines](https://img.shields.io/tokei/lines/github/caipeide/autorace)
![last_update](https://img.shields.io/github/last-commit/caipeide/autorace)
[![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Autonomous%20RC-Car%20Racing%20Competition%20in%20HKUST&url=https://github.com/caipeide/autorace&hashtags=rc_car,jetson_nano,deep_learning,visual_navigation,hkust)

</div>

<div align=center>
<img src=images/demo.gif width="70%">
</div>

Autorace provides hardware and example codes to achieve vision-based autonomous racing on RC-Cars. It is developed by [RAM-LAB](https://www.ram-lab.com/) to support *the 1st autonomous RC-Car racing competition* in Hong Kong University of Science and Technology (HKUST). The competition data is Feb 26, 2021 (tentative, due to COVID-19).

**Event Collaborators**: School of Engineering, Robotics Institue (RI), Robotics and Multiperception Lab (RAM-LAB), Intelligent Autonomous Driving Center, Entrepreneurship Center

**Keywords:** autonomous racing, visual navigation, artifical intelligence, deep learning.

**Maintaners:** [Peide Cai](https://www.ram-lab.com/people/#mr-peide-cai) &lt;pcaiaa@connect.ust.hk&gt;

💻 [Official Website](https://ecenter.ust.hk/events/hkust-autonomous-rc-car-racing-competition)

📹 [Demo & Workshops](https://sites.google.com/view/autorc-racing/)

🏁 [Rules and Regulations](https://www.ec.ust.hk/sites/default/files/1/HKUST%20Autonomous%20RC-car%20Racing%20Competition_1.pdf)

If you like the project, give it a star ⭐. It means a lot to the people maintaining it 🧙.

# Table of Contents <!-- omit in toc --> <span id=table-of-contents>
- [Features](#features)
- [Build a RC-Car](#build-a-rc-car)
- [System Installation](#system-installation)
  - [1. Jetson Nano on the RC-Car](#1-jetson-nano-on-the-rc-car)
    - [1.1 Use JetPack to Install a Base Ubuntu System](#11-use-jetpack-to-install-a-base-ubuntu-system)
      - [1.1.1 Features](#111-features)
      - [1.1.2 Installation](#112-installation)
      - [1.1.3 Caution](#113-caution)
    - [1.2 Use JetCard to Quickly Configure the System](#12-use-jetcard-to-quickly-configure-the-system)
      - [1.2.1 Features](#121-features)
      - [1.2.2 Installation](#122-installation)
      - [1.2.3 Tips](#123-tips)
  - [2. Your Host PC](#2-your-host-pc)
    - [2.1 Requirement](#21-requirement)
    - [2.2 Graphics Driver Installation](#22-graphics-driver-installation)
    - [2.3 System Configuration](#23-system-configuration)
      - [2.3.1 Features](#231-features)
      - [2.3.2 Installation](#232-installation)
    - [2.4 Test: Remote Connection between Host PC (or server) and RC-Car](#24-test-remote-connection-between-host-pc-or-server-and-rc-car)
      - [2.4.1 RC-Car <--> Host PC](#241-rc-car----host-pc)
      - [2.4.2 Server Account <--> Host PC](#242-server-account----host-pc)
- [Train a Self-driving Car](#train-a-self-driving-car)
  - [1. Car Steering Calibration](#1-car-steering-calibration)
  - [2. Data Collection](#2-data-collection)
  - [3. Model Training](#3-model-training)
    - [3.1 Accelerate your Model](#31-accelerate-your-model)
  - [4. Model Testing](#4-model-testing)
- [Notes](#notes)
- [Other Useful Toturials](#other-useful-toturials)
  - [Python3](#python3)
  - [PyTorch](#pytorch)
- [Credits](#credits)
  
## Features
* Coding language: *Python3*
* Deep learning framework: [*PyTorch 1.6*](https://pytorch.org/)
* On-board computer: [*Jetson Nano B1*](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-nano/)
* Complete pipeline of data collection, model training and testing
* Easy to use and DIY
* What can you achieve 🤔?

    1. Build a small but powerful RC-Car that can drive itself.
    2. Record driving data (camera images, control actions) by teleoperating the RC-Car.
    3. Train different AI autopilots to autonomously drive your car on the track as fast as possible.
    4. Autonomous collision avoidance around different obstacles.


## Build a RC-Car

The RC-Car is named JetRacer, a high speed AI racing robot powered by Jetson Nano. 

<div align=center>
<img src=images/car.jpg width="60%">
</div>

<div align=center>
<img src=images/components.jpg width="100%">
</div>

**Website**: [中文](https://www.waveshare.net/shop/JetRacer-Pro-AI-Kit.htm) | [EN](https://www.waveshare.com/product/ai/robots/mobile-robots/jetracer-pro-ai-kit.htm) 

**JetRacer WiKi**: [中文](https://www.waveshare.net/wiki/JetRacer_Pro_AI_Kit) | [EN](https://www.waveshare.com/wiki/JetRacer_Pro_AI_Kit)

> Some parts of the user guides on software in the above wiki (provided by the vendor) are out-of-date (you may meet different errors during tests). Please follow this repository for system and software installation in the following sections, and just take the above wiki as a reference.

**Assemble Manusal**: [中文](images/Jetracer_pro_Assembly_CN.pdf) | [EN](images/Jetracer_pro_Assembly_EN.pdf) 

**Slides and Assemble Video**: [Link](https://sites.google.com/view/autorc-racing/workshops#h.2vgfpvidyayt)

<div align=center>
<img src=images/car_composing.gif width="65%">
</div>

[Back to Top](#table-of-contents)

## System Installation

### 1. Jetson Nano on the RC-Car 
> This is for data collection and model deployment, covered in our [2nd workshop](https://sites.google.com/view/autorc-racing/workshops?authuser=0#h.k8kmaurf4zv0) with slides and videos.

[NVIDIA Jetson Nano](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-nano/) lets you bring incredible new capabilities to millions of small, power-efficient AI systems. It is also the perfect tool to start learning about AI and robotics in real-world settings, with ready-to-try projects and the support of an active and passionate developer community. 

<div align=center>
<img src=images/jetson_nano.jpg width="50%">
</div>

To use this mainboard, we need to install a software development kit on it, which is named JetPack 👇

#### 1.1 Use JetPack to Install a Base Ubuntu System


##### 1.1.1 Features
> Based on the introduction in https://developer.nvidia.com/jetpack-sdk-44-archive

[JetPack SDK](https://developer.nvidia.com/jetpack-sdk-44-archivek) is the most comprehensive solution for building AI applications. It includes the latest Linux Driver Package (L4T) with Linux operating system named Ubuntu (version: 18.04) and CUDA-X accelerated libraries and APIs for Deep Learning, Computer Vision, Accelerated Computing and Multimedia. It also includes samples, documentation, and developer tools for both host computer and developer kit. 

*In this project we use [JetPack 4.4](https://developer.nvidia.com/jetson-nano-sd-card-image-44
).*

##### 1.1.2 Installation

JetPack installation is quite simple: Flash the image to a microSD card -> Connect Nano to a display and boot the system (Ubuntu 18.04) -> Finish initialization. **Step-by-step instructions** are from Page 4 - Page 23 in [this slides](https://sites.google.com/view/autorc-racing/workshops?authuser=0#h.k8kmaurf4zv0) from workshop#2. Then you will enter the Ubuntu 18.04 system, which looks like the following:

<div align=center>
<img src=images/jetpack.png width="70%">
</div>

##### 1.1.3 Caution

Remember do not upgrade the system after installation, even the system reminds you of that. Because some of our library dependencies rely on the current version of jetpack, which is 4.4.


#### 1.2 Use JetCard to Quickly Configure the System

After installing the Ubuntu 18.04 system with JetPack4.4, we provide a system configuration named JetCard to make it easy to get started with AI on Jetson Nano. Simply execute the provided script and all external library dependencies will be installed automatically.

##### 1.2.1 Features

JetCard comes pre-loaded with:

* A Jupyter Lab server that starts on boot for easy web programming
* A script to display the Jetson Nano's IP address, CPU & GPU usage, battery life, charging status, etc.
* The popular deep learning frameworks [PyTorch](https://pytorch.org/) (version: 1.6)
* A Python3 library to drive RC-Cars [Donkeycar](https://github.com/caipeide/donkeycar)
* Other development tools such as [Oh My Zsh](https://github.com/ohmyzsh/ohmyzsh), [virtualenv](https://pypi.org/project/virtualenv/), [torch2trt](https://github.com/NVIDIA-AI-IOT/torch2trt)

After configuring your system using JetCard, you can get started prototyping AI projects from your web browser in Python3.

##### 1.2.2 Installation


After you install [JetPack 4.4](https://developer.nvidia.com/jetpack-sdk-44-archive) on the SD card, boot the system (Ubuntu 18.04) and open a terminal by pressing `Ctrl+Alt+T`, and then do the followings to use JetCard to quickly configure your system:

```console
$ cd ~
$ git clone https://github.com/caipeide/jetcard
$ cd jetcard
$ sh ./install.sh <password>
```

<div align=center>
<img src=images/jetcard_install.gif width="80%">
</div>


The whole installation will cost about 40 min. After that the script will ask you to reboot. Take a look at the ip address shown on the display (10.79.157.13 in this case).

<div align=center>
<img src=images/display.jpg width="50%">
</div>

Now you can disconnect the HDMI port, keyboard and mouse on the jetson nano and start remote development: Open a browser on your own laptop and enter `10.79.157.13:8888` for remote connection to and development on the car. (the `<password>` you set earlier will be asked to enter the jupyterlab)

<div align=center>
<img src=images/jupyterlab.png width="80%">
</div>

##### 1.2.3 Tips

To ensure that the Jetson Nano doesn't draw more current than the battery pack can supply, place the Jetson Nano in 5W mode by calling the following command.

- You need to launch a new Terminal (by pressing `Ctrl+Alt+T`) and enter following commands to select 5W power mode:
```console
$ sudo nvpmodel -m1
```
- Check if mode is correct (or take a look at the car display):
```console
$ sudo nvpmodel -q
```
*m1: 5W power mode, m2: 10W power mode (MAXN)*

[Back to Top](#table-of-contents)

### 2. Your Host PC
> This is for model training

#### 2.1 Requirement

* Nvidia GPU (at least with 6 GB frame buffer), e.g., RTX 2060, GTX 1080.
* Ubuntu 18.04 system should be installed.

*For the participants who do not have a NVIDIA graphics card (GPU) in their computer, they can apply for using our server to train their models, and skip the following section 2.2*

#### 2.2 Graphics Driver Installation

> The following instructions refer to steps from [2 Ways to Install Nvidia Driver on Ubuntu 18.04 (GUI & Command Line)](https://www.linuxbabe.com/ubuntu/install-nvidia-driver-ubuntu-18-04). Here we simply choose to use graphical user interface (GUI) for installing the Nvidia driver.

First, go to `system settings` > `details` and check what graphics card your computer is using. By default, your integrated graphics card (Intel HD Graphics) is being used.

<div align=center>
<img src=images/nvidia_driver_1.png width="80%">
</div>

Then open `softare & updates` program from you application menu. Click the `additional drivers` tab. You can see what driver is being used for Nvidia card. If you can not see `nvidia-driver-xxx` in the list, open a terminal and do `sudo apt update`, then re-open this window, and available drivers can be updated.

<div align=center>
<img src=images/nvidia_driver_0.png width="80%">
</div>

<div align=center>
<img src=images/nvidia_driver_2.png width="80%">
</div>

As you can see many driver versions are available for the GeForce RTX 2080 Ti card on our server. Here we use the `nvidia-driver-440` and it works fine for our model training. There might be some other drivers for your particular Nvidia card. Click `Apply Changes` button to install the driver.

After it’s installed, reboot your computer for the change to take effect. After that, go to `system settings` > `details`, you will see Ubuntu is using Nvidia graphics card.

<div align=center>
<img src=images/nvidia_driver_3.png width="80%">
</div>

You can open a terminal and do `nvidia-smi` to check the running information of your GPU:

<div align=center>
<img src=images/nvidia-smi.png width="80%">
</div>

#### 2.3 System Configuration

We provide a script `install_host.sh` for you to quickly configure your host PC (or server account) with all necessary dependencies for model training.

##### 2.3.1 Features

By executing the script, the following packages will be automatically installed:

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html): A package manager that helps you find and install packages. Then a new conda environement named `autorace` will be automatically created
- OpenCV: An open source computer vision and machine learning software library. 
- Matplotlib: A comprehensive library for creating static, animated, and interactive visualizations in Python.
- Other tools such as Pytorch 1.6 and [Oh My Zsh](https://github.com/ohmyzsh/ohmyzsh)

After configuring your system using `install_host.sh`, you can get started copying data between your host PC (or server account) and your RC-Car, and using the collected dataset to train your own self-driving car (will be introduced in the next section [Train a Self-driving Car](#train-a-self-driving-car))

##### 2.3.2 Installation
```console
$ cd ~
$ sudo apt install git
$ git clone https://github.com/caipeide/autorace
$ cd autorace
$ sh ./install_host.sh
$ source ~/.bashrc
$ conda create -n autorace python=3.6 -y
$ conda activate autorace
$ sh ./install_host_continue.sh
```
*Note*: The second command `sudo apt install git` is not needed on our server.

#### 2.4 Test: Remote Connection between Host PC (or server) and RC-Car

##### 2.4.1 RC-Car <--> Host PC 

##### 2.4.2 Server Account <--> Host PC 
```console
$ ssh -p 1234 team1@xx.xx.xx.xx
```
[Back to Top](#table-of-contents)

## Train a Self-driving Car

### 1. Car Steering Calibration

### 2. Data Collection
Randomly place different obstacles on the track.

```console
$ python manage.py drive --js
```

### 3. Model Training
```console
$ python manage.py train --model models/resnet18.pth --type resnet18
```

#### 3.1 Accelerate your Model
```console
$ python accel_model.py --model models/resnet18.pth --half --type resnet18
```
### 4. Model Testing
```console
$ python manage.py drive --model models/resnet18_trt.pth --half --trt --type resnet18
```

## Notes

1. Do not directly turn off the power when system is running. Open a terminal and do`sudo shutdown`first to shutdown the OS system, then turn off the power.
2. If the RC-Car crashes into the track fence at a high speed, the front wheels are likely to get stuck at their drive rods. Then you have to remove the two drive rods and reinstall them, which is a little troublesome. *It is suggested to simply removing the drive rod of the two front wheels, then this problem can be solved.* **Other hardware modifications are not allowed.**
3. You are free to DIY your own algorithms to drive the car for competition, but the following functions in this repo should be kept:
   1. Press `ENTER` to start the car immediately when using autopilot mode

## Other Useful Toturials

### Python3
- [EN](https://www.learnpython.org/)
- [中文](https://www.liaoxuefeng.com/wiki/1016959663602400)

### PyTorch
- https://github.com/MorvanZhou/PyTorch-Tutorial
- https://github.com/yunjey/pytorch-tutorial
- https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html


## Credits
* [Donkeycar](https://github.com/autorope/donkeycar): Open source hardware and software platform to build a small scale self driving car.
* [JetRacer](https://github.com/NVIDIA-AI-IOT/jetracer): An autonomous AI racecar using NVIDIA Jetson Nano.
* [Jetcard](https://github.com/NVIDIA-AI-IOT/jetcard/tree/jetpack_4.4): An SD card image for web programming AI projects with NVIDIA Jetson Nano.
* [torch2trt](https://github.com/NVIDIA-AI-IOT/torch2trt): An easy to use PyTorch to TensorRT converter for model acceleration. Real-time computing performance is important for our high-speed driving occasions.
* [Getting Started with Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#intro)