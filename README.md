<div align=center>
<img src=images/logo.png width="65%">

![license](https://img.shields.io/github/license/caipeide/autorace)
![code_size](https://img.shields.io/github/languages/code-size/caipeide/autorace)
![total_Lines](https://img.shields.io/tokei/lines/github/caipeide/autorace)
[![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Autonomous%20RC-Car%20Racing%20Competition%20in%20HKUST&url=https://github.com/caipeide/autorace&hashtags=rc_car,jetson_nano,deep_learning,visual_navigation,hkust)

</div>

<div align=center>
<img src=images/demo.gif width="70%">
</div>

Autorace provides hardware and example codes to achieve vision-based autonomous racing on RC-Cars. It is developed by [RAM-LAB](https://www.ram-lab.com/) to support *the 1st autonomous RC-Car racing competition* in Hong Kong University of Science and Technology (HKUST). The competition data is Feb 26, 2021 (tentative, due to COVID-19).

**Event Collaborators**: School of Engineering, Robotics Institue (RI), Robotics and Multiperception Lab (RAM-LAB), Intelligent Autonomous Driving Center, Entrepreneurship Center

**Keywords:** autonomous racing, visual navigation, artifical intelligence, deep learning.

**Maintaners:** [Peide Cai](https://scholar.google.com/citations?user=D4YzMA8AAAAJ&hl=en) &lt;pcaiaa@connect.ust.hk&gt; &emsp; **Supervisor:** [Prof. Ming Liu](https://www.ram-lab.com/people/#dr-ming-liu-director) &lt;eelium@ust.hk&gt;

💻 [Official Website](https://ecenter.ust.hk/events/hkust-autonomous-rc-car-racing-competition)

📹 [Demo & Workshops](https://sites.google.com/view/autorc-racing/)

🏁 [Rules and Regulations](https://www.ec.ust.hk/sites/default/files/1/HKUST%20Autonomous%20RC-car%20Racing%20Competition_1.pdf)

If you meet with any problems, feel free to create an [issue](https://github.com/caipeide/autorace/issues) to let me and other participants know, then we can solve it together.

If you like the project, give it a star ⭐. It means a lot to the people maintaining it 🧙

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
- [Start Your Journey of Self-Driving](#start-your-journey-of-self-driving)
  - [1. Calibration](#1-calibration)
    - [1.1 Configuration Files](#11-configuration-files)
    - [1.2 Throttle Calibration](#12-throttle-calibration)
    - [1.3 Steering Calibration](#13-steering-calibration)
    - [1.4 Fine Tuning and Testing Your Calibration](#14-fine-tuning-and-testing-your-calibration)
  - [2. Data Collection](#2-data-collection)
    - [2.1 Driving with Web Controller](#21-driving-with-web-controller)
      - [2.1.1 Features](#211-features)
      - [2.1.2 Keyboard Shortcuts](#212-keyboard-shortcuts)
    - [2.2 Driving with Physical Joystick Controller](#22-driving-with-physical-joystick-controller)
      - [2.2.1 Features](#221-features)
      - [2.2.2 Start the Programm for Data Collection](#222-start-the-programm-for-data-collection)
      - [2.2.3 Data Collection Procedure](#223-data-collection-procedure)
      - [2.2.4 Tips](#224-tips)
  - [3. Model Training](#3-model-training)
    - [3.1 Transfer Data from RC-Car to Host PC](#31-transfer-data-from-rc-car-to-host-pc)
    - [3.2 Start Training Models](#32-start-training-models)
    - [3.3 Copy Model Back to RC-Car](#33-copy-model-back-to-rc-car)
    - [3.4 Accelerate your Model](#34-accelerate-your-model)
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

<div align=center>
<img src=images/do_not_upgrade.png width="80%">
</div>


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

Finally, we clone this project to the RC-Car:

```console
$ cd ~/projects/donkeycar
$ pip install -e .
$ cd ~
$ git clone https://github.com/caipeide/autorace
```

<div align=center>
<img src=images/sys_config.png width="80%">
</div>

##### 1.2.3 Tips

To ensure that the Jetson Nano doesn't draw more current than the battery pack can supply, place the Jetson Nano in 5W mode by calling the following command.

- You need to launch a new Terminal and enter following commands to select 5W power mode:

<div align=center>
<img src=images/open_terminal.png width="80%">
</div>

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
> A host PC is needed for model training

#### 2.1 Requirement

* Nvidia GPU (at least with 6 GB frame buffer), e.g., RTX 2060, GTX 1080.
* Ubuntu 18.04 system should be installed.

*For participants who do not have a NVIDIA graphics card (GPU) in their computer, they can apply for using our server to train their models, and skip the following section 2.2. In this way, the laptop will be only used for remote connection to the RC-Car, which is doable on any system including Windows, MacOS and Ubuntu.*

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
- OpenCV: An open source computer vision and machine learning software library
- Matplotlib: A comprehensive library for creating static, animated, and interactive visualizations in Python
- Other tools such as Pytorch 1.6 and Donkeycar

After configuring your system, you can get started transmitting data between your host PC (or server account) and your RC-Car (via `ssh`), and using the collected dataset to train your own self-driving car (will be introduced in the next section [Train a Self-driving Car](#train-a-self-driving-car))

##### 2.3.2 Installation

1. If you are using your own PC, open a terminal and do the first three steps first in the following (they are already installed on the server)

```console
$ sudo apt update
$ sudo apt install openssh-server
$ sudo apt install git
```
2. Then you can install the other dependencies.

>If you are using the server, connect to it with `ssh` first in a new terminal on your PC (or on the RC-Car with jupyterlab), for example, If you are using Ubuntu, open a new terminal (`Ctrl+Alt+T`) and `ssh -p <port_number> <server_account_name>@<server_ip_address>`. Then do the followings in the terminal for host configuration.

```console
$ cd ~
$ git clone https://github.com/caipeide/autorace
$ cd autorace
$ sh ./install_host.sh
$ source ~/.bashrc
$ conda create -n autorace python=3.6 -y
$ conda activate autorace
$ sh ./install_host_continue.sh
```


[Back to Top](#table-of-contents)

## Start Your Journey of Self-Driving

### 1. Calibration

#### 1.1 Configuration Files 

All of the car's settings are in the `config.py` and `myconfig.py` scripts. `config.py` stores the default values for all parameterss, and you can adjust these settings in `myconfig.py` by *uncommenting* related lines and *changing* their values. When the main program `manage.py` starts, it will first read `config.py` and then override the variables with values you set in `myconfig.py`. 

You can edit this file using two methods:

- If you are in a terminal, you can use [nano](https://serverpilot.io/docs/how-to-use-nano-to-edit-files/) to edit files:

```console
nano ~/autorace/myconfig.py
```

- If you perfer GUI, you can directly edit files in Jupyter Lab. Just double-click a file, make changes, and `Ctrl+S` to save.

Here *uncomment* means deleting the `#` symbol at the beginning of lines. In most editors, you can toggle between the *comment* and *uncomment* status by pressing `Ctrl+/`.

#### 1.2 Throttle Calibration

> Make sure your car is off the ground to prevent a runaway situation.

<div align=center>
<img src=images/off_the_ground.jpg width="50%">
</div>

1. Turn on your car and the motor, and connect to the car via Jupter Lab on your PC.
2. Open a terminal and run `donkey calibrate --channel 1 --bus=1`
3. Enter `370` when prompted for a PWM value. Then you should hear your ESC **beep** indicating that it's calibrated. If not, adjust this value a little, or else the motor won't work.
4. Enter 400 and you should see your cars wheels start to go forward.
5. Keep trying different values until you've found a reasonable max speed and remember this PWM value. *Remember do not set the max speed too high, otherwise, the front wheel of the car will be easily damaged when crashed at fence.* For repairing, refer to [this](#notes-repair).

Reverse on RC cars is a little tricky because the ESC must receive a reverse pulse, zero pulse, reverse pulse to start to go backwards. To calibrate a reverse PWM setting...

1. Enter the reverse value, for example `330`, then the zero throttle value you find above, then the reverse value again.
2. Enter values +/- 10 of the reverse value to find a reasonable reverse speed. Remember this reverse PWM value.

Enter these values in `myconfig.py` script as `THROTTLE_FORWARD_PWM`, `THROTTLE_STOPPED_PWM`, and `THROTTLE_REVERSE_PWM`.

#### 1.3 Steering Calibration

2. Open a terminal and run `donkey calibrate --channel 0 --bus=1`
3. Enter 320 and you should see the wheels on your car move slightly. If not enter 400 or 300.
4. Next enter values +/- 10 from your starting value to find the PWM setting that makes your car turn all the way left and all the way right. Remember these values.
5. Enter these values in `myconfig.py` script as `STEERING_RIGHT_PWM` and `STEERING_LEFT_PWM`. Note that the default vaules are `STEERING_LEFT_PWM = 460`,
`STEERING_RIGHT_PWM = 290`, saved in `config.py`.

**Note**: You need to make sure that the value `(STEERING_LEFT_PWM + STEERING_RIGHT_PWM)*0.5` can make the front wheels face straight ahead, then the car can drive in a straight line with `steering = 0`.

#### 1.4 Fine Tuning and Testing Your Calibration

Now that you have your car roughly calibrated you can try driving it to verify that it drives as expected. Here's how to fine tune your car's calibration. 

1. Start your car by running `python manage.py drive` in this folder.
2. Go to `<car_ip_address>:8887` in a browser (Tested on [Chrome](https://www.google.com/chrome/)). The following is what you will see: camera video streams, adjustable control values and driving modes. Now you can press `J` or `L` on keyboard to adjust the car steering to left or right, and use `I` and `K` to adjust the throttle values.

<div align=center>
<span id=drive-ui>
<img src=images/drive_UI.png width="70%">
</div>


3. Now set the steering to *zero* and press `I` a few times to get the car to go forward. If it goes straight, that is good and you can move on to the next section; if not, adjust your values of `STEERING_LEFT_PWM` and `STEERING_RIGHT_PWM` until a straight driving trajectory can be achieved.

**Note**: Too small throttle values, e.g., 0.1, may not be enough to drive the car. You need to increase it a bit.


### 2. Data Collection

#### 2.1 Driving with Web Controller
> Only for basic testing. If you want to collect data in a more flexible way, use the joystick introduced in the next section [Driving with Physical Joystick Controller](#22-driving-with-physical-joystick-controller)

This controller provides a [UI window](#drive-ui) accessible at `<car_ip_address>:8887`. After you run `python manage.py drive` this module will be loaded.

##### 2.1.1 Features

- *Pilot mode* - Choose this if the pilot should control the angle and/or throttle. It has three options: 
  - `local_angle` will only let the pilot model control the angle of the car.
  - `local_pilot` will let the pilot model control both the angle and throttle. 
  - `user_mode` where you have full control over the car using keyboard shortcuts or mouse.
  
  &nbsp;&nbsp;&nbsp;**Notes**
  - Switches to pilot modes will only take effect if you load your neural network model when starting the `manage.py`, which will be introduced in [Model Testing](#4-model-testing).
  - Clicking with mouse on the right blue area (with texts "Click/touch to use joystic") will switch from `pilot` modes to `user_mode`. You can use this function to quickly stop your self-driving car.

- *Recording* - Press record data to start recording images, steering angels and throttle values. By default the data will be automatically recorded if throttle is not zero in `user_mode`. If the car is in pilot mode, you can use this function to manually record some self-driving data. **Note** do not use the data from a pilot mode to train you netowrk. Training details will be covered in [Model Training](#3-model-training).
  
- *Throttle mode* - Option to set the throttle as constant. This is used in races if you have a pilot that will steer but doesn't control throttle.

- *Max throttle* - Select the maximum throttle for `user_mode`.

##### 2.1.2 Keyboard Shortcuts

- `R` : toggle recording
- `I` : increase throttle by 0.05
- `K` : decrease throttle by 0.05
- `J` : turn left
- `L` : turn right

**Note**: Throttle range and steering range are both [-1.0, 1.0]. Throttle values that are less than 0 indicate reversing.

#### 2.2 Driving with Physical Joystick Controller

##### 2.2.1 Features

- Recommended for data collection, much more flexible to operate the RC-Car than using web controller.
- By default, no UI interface is published in this mode. However, you can set `USE_FPV = True` in `myconfig.py` to monitor the camera video streams. The published FPV images are accessible in `<car_ip_address>:8890`

##### 2.2.2 Start the Programm for Data Collection

- Plug the USB receiver of the Joystick controller into Jetson Nano, then start the program (before that, make sure your car motor is powered on):

```console
$ cd ~/autorace
$ python manage.py drive --js
```
> Optionally, if you want joystick use to be sticky and don't want to add the `--js` each time, modify your `myconfig.py` so that `USE_JOYSTICK_AS_DEFAULT = True`

- The joystick controls are shown as follows, they will also be printed on your sceen when the program starts.

```console
+------------------+--------------------------+
|     control      |          action          |
+------------------+--------------------------+
|     a_button     |       toggle_mode        |
|     b_button     | toggle_manual_recording  |
|     x_button     |   erase_last_N_records   |
|     y_button     |      emergency_stop      |
|  right_shoulder  |  increase_max_throttle   |
|  left_shoulder   |  decrease_max_throttle   |
|     options      | toggle_constant_throttle |
| left_stick_horz  |       set_steering       |
| right_stick_vert |       set_throttle       |
|  right_trigger   |    constant_rage_mode    |
|   left_trigger   |   constant_gentle_mode   |
+------------------+--------------------------+
```

<div align=center>
<img src=images/joystick.png width="80%">
</div>


- Explanations on the operations.
  - `left_stick_horz`: Left analog stick - Left and right to adjust steering
  - `right_stick_vert`: Right analog stick - Forward to increase forward throttle, and Backward to increase reverse throttle. No operation for zero throttle.
  - `toggle_mode`: Switches modes - "User, Local Angle, Local(angle and throttle)"
  - `toggle_manual_recording`: Toggle recording of all data even if your car stops with zero throttle. This is disabled by default because a more suitable method *auto record on throttle* is enabled by default, which means that whenever the throttle is not zero, driving data will be recorded - as long as you are in user mode. The data will be saved in folder `data/tub_xx_xx_xx/` 
  - `erase_last_N_records`: You don't want to use bad data to train you network, such as collisions with walls. This function can erase the data in the last 100 frames to keep your dataset clean.
  - `increase_max_throttle`: the max_throttle for joystick control is set to 0.5 by default (when right analog stick is pushed to the front). Press right shoulder to increase the max_throttle by `PER_THROTTLE_STEP` if you need more speed. `PER_THROTTLE_STEP` is 0.05 by default, you can change this in `myconfig.py`.
  - `decrease_max_throttle`: Simmilar to the above. Press left shoulder to decrease the max_throttle by `PER_THROTTLE_STEP`.
  - `toggle_constant_throttle`: Toggle constant throttle. Sets to max throttle.
  - `constant_rage_mode`: Start a constant throttle mode with very a large throttle `RAGE_THROTTLE = 0.75`. This can be useful at long and straight tracks, where you can quickly accelerate your car. The throttle value can be adjusted in `myconfig.py`
  - `constant_gentle_mode`: Start a constant throttle mode with a low throttle `GENTLE_THROTTLE = 0.45`. This can be useful when RC-Car enters a sharp corner at high speeds, where you need to quickly slow the speed down but not stop. This throttle can also be adjusted in `myconfig.py`



##### 2.2.3 Data Collection Procedure

1. Place some obstacles on the track, and practice driving around the track a couple times. Considering you may not drive well at first, you can set `AUTO_RECORD_ON_THROTTLE = False` in `myconfig.py` to disable recording data automatically.
2. When you're confident you can drive 10 laps without mistake, restart the python `mange.py` process to create a new tub session. Set `AUTO_RECORD_ON_THROTTLE = True`. The joystick will auto record with any non-zero throttle.
3. If you crash or run off the track, loosen the throttle immediately to stop recording. Then tap the X button to erase the last 5 seconds of records.
4. After you've collected 10-20 laps of good data (5-20k images) you can stop your car with `Ctrl+C` in the terminal session for your car. 
5. The data you've collected is in the `data/` folder in the most recent tub folder.

>After you finish training a car can that can drive solely on the track based on the following procedure, **you should return to this part and cooperate with another team** to collect data on wheel-to-wheel driving (two cars running on the track). These data will be **crucial** for your model to learn how to behave in the presence of another car, such as overtaking and slowing down to avoid collisions. Otherwise, it is likely to perform poorly in the main race.

##### 2.2.4 Tips

- To increase the robustness of your model, you should place different obstacles (colors, types) randomly on diffeent locations on the track during data collection.
- `DRIVE_LOOP_HZ` set in `myconfig.py` is the max frequency that the drive loop should run. The actual frequency may be less than this if there are many blocking parts, e.g., your designed AI model is too complex to run quickly.
- You can choose whether or not to add extra control noise in `user_mode`. If the value `CONTROL_NOISE` is set to `True` in `myconfig.py` (default value is `False`), random action noises on steering angle and throttle will be added during your tele-operation. This can help you to collect more divrese data that the car recovers from off-center and off-orientation mistakes. Based on these your trained agent can be more "intelligent". We also provide two scalars `THROTTLE_NOISE` and `ANGLE_NOISE` to adjust the level of noise. Note with this module acctivated, the data collection process will be difficult.


### 3. Model Training

#### 3.1 Transfer Data from RC-Car to Host PC

Training a deep neural network on Jetson Nano can be painful (quite slow 🐌). Therefore, we will use more powerful PCs for faster training. The first step is to copy the collected data from your RC-Car to the host PC.

1. If you are using your own computer for model training, open a new terminal on your host PC and use `rsync` to copy your cars `data/` folder.

```console
$ cd ~/autorace
$ rsync -rv --progress --partial <car_account_name>@<car_ip_address>:~/autorace/data ./
```

2. If you use the server for model training, open a new terminal on the RC-Car, then do the followings instead.

```console
$ cd ~/autorace
$ rsync -rv -e 'ssh -p <port_number>' --progress --partial ./data <server_account_name>@<server_ip_address>:~/autorace/
```

Now you can check the new data in the folder `~/autorace/data/` on your host PC:

```console
$ ssh -p <port_number> <server_account_name>@<server_ip_address>  # if you use the server, connect to it via ssh first on your RC-Car
$ ls ~/autorace/data/
```
The copied data folders will be printed. The following is an example.

<div align=center>
<img src=images/transfer_data.png width="80%">
</div>

#### 3.2 Start Training Models

In the same terminal you can now run the training script on the latest tub by passing the path to that tub as an argument. For example,

```console
$ cd ~/autorace
$ python manage.py train --model models/resnet18.pth --type resnet18 --tub data/tub_1_20-12-12/,data/tub_2_20-12-12
```
The trained model will be saved in `~/autorace/models/resnet18.pth`. Optionally you can pass no arguments for the tub, and then all tubs will be used in the default `data/` folder.

```console
$ python manage.py train --model models/resnet18.pth --type resnet18
```

We provide three basic model types for training: *[linear](https://images.nvidia.com/content/tegra/automotive/images/2016/solutions/pdf/end-to-end-dl-using-px.pdf), [rnn](https://blog.floydhub.com/a-beginners-guide-on-recurrent-neural-networks-with-pytorch/) and [resnet18](https://arxiv.org/pdf/1512.03385.pdf)*. Click these hyperlinks for more details. The following image shows the model architecture from [Nvidia Self-Driving Car](https://developer.nvidia.com/blog/deep-learning-self-driving-cars/f) in 2016, which uses a series of convolutional layers and fully connected layers to learn driving behaviors.

<div align=center>
<img src=images/linear_model.png width="50%">
</div>

You can change these model architectures in `ai_drive_models.py`, where `linear -> LinearModel`, `rnn -> RNNModel` and `resnet18 -> LinearResModel`. Note the rnn model runs slowly on the RC-Car, thus it may not be suitable for racing.

Other training parameters such as batchsize, learning rate, etc., can be configured in `myconfig.py`. Their default values should work well in most cases.

During training you can run `nvidia-smi` in a terminal to check GPU power consumption and memory usage. The following shows a training demo.

<div align=center>
<img src=images/model_training.gif width="100%">
</div>

After the training is finished, you can view how the training loss and validation loss decrease in `models/loss_plot_resnet18.png`.

<div align=center>
<img src=images/loss_plot.png width="70%">
</div>

#### 3.3 Copy Model Back to RC-Car

In previous step we managed to get a model trained on the data. Now is time to move the model back to RC-Car, so we can use it for testing it if it will drive itself.

1. If you use your own computer for model training, open a new terminal on your host PC:

```console
$ cd ~/autorace
$ rsync -rv --progress --partial ./models/resnet18.pth <car_account_name>@<car_ip_address>:~/autorace/models/
```

2. If you use the server for model training, open a new terminal on the RC-Car, then do the followings instead.

```console
$ cd ~/autorace
$ rsync -rv -e 'ssh -p <port_number>' --progress --partial <server_account_name>@<server_ip_address>:~/autorace/models/resnet18.pth ./models/
```

#### 3.4 Accelerate your Model

The `resnet18` model trained above runs about 150 ms/frame (6.7 Hz) on the car, which can cause problems if your car drives fast (not quickly enough to make a decision to take turns -> collision). Therefore, we will accelerate the model as follows on the RC-Car:

```console
$ cd ~/autorace
$ python accel_model.py --model models/resnet18.pth --type resnet18
```

The process takes about 1 ~ 2 min, and the accelerated model will be saved in `models/resnet18_trt.pth`. The inference speed of this model is about 50 ms/frame (20 Hz).

Notes:
1) You may have some problems if you try to acclerate a rnn model, which seems to be the limitation of the `torch2trt` library we use. Unfortunately, I have no solution on that.
2) Add `--half` to the above command if you want to save memory usage of the neural network. Then the accelerated model will be using FP16 rather than FP32, allowing deployment of larger networks.

### 4. Model Testing

>Ensure to place the car on the track and power on its motor so that it is ready to drive.

```console
$ python manage.py drive --model models/resnet18_trt.pth --trt --type resnet18
```
When all modules are ready (1 ~ 2 min to warm up), the program will notice you to press `ENTER` to start. Then the car should start to drive on it's own. Congratulations!

Notes:

1) Add `--half` to the above command if you use that during model acceleration.

[Back to Top](#table-of-contents)

## Notes

1. The ip address of the car may change automatically (it will change only once after each boot). If your JupyterLab losts connection, check if the car's ip is changed. If so, using the new ip to refresh the browser.
2. If you collect lots of data, for example, more than 1000 images in a tub under `data/` folder, DO NOT try to open the tub folder and view images through JupyerLab, because it will cost much time to load the files and the GUI may freeze. You can transfer the data to your laptop to view.
3. Do not directly turn off the power when system is running. Open a terminal and do`sudo shutdown`first to shutdown the OS system, then turn off the power.
4. <span id=notes-repair>If the RC-Car crashes into the track fence at a high speed, the front wheels are likely to get stuck at their drive rods. Then you have to take off the two drive rods and reinstall them, which is a little troublesome. *It is suggested to simply removing the drive rod of the two front wheels, then this problem can be solved.* [This video demonstrates how to fix the problem](https://youtu.be/y_o_JfhMo50). **Other hardware modifications are not allowed.**
5. You are free to DIY your own algorithms to drive the car for competition, but the following functions in this repo should be kept:
   1. Press `ENTER` to start the car immediately when using autopilot mode
6. If you think coding with Jupyter Lab is boring because it lacks code navigation functins like `go to defination` and `code suggestions`, you can choose [VSCode](https://code.visualstudio.com/) for development.
   
>Visual Studio Code has a high productivity code editor which, when combined with programming language services, gives you the power of an IDE and the speed of a text editor. [In this topic](https://code.visualstudio.com/docs/editor/editingevolved#_quick-file-navigation), we'll first describe VS Code's language intelligence features (suggestions, parameter hints, smart code navigation) and then show the power of the core text editor.

After installation, you can install the [`Remote - SSH`](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) extension within VSCode to let your editor connected to your RC-Car. The following is a video demo showing how.

<div align=center>
<img src=images/remote-ssh.gif width="100%">
</div>


[Back to Top](#table-of-contents)

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