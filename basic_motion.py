#!/usr/bin/env python3
import os
import time
import numpy as np
import donkeycar as dk
from donkeycar.parts.controller import LocalWebController, JoystickController, WebFpv
from tools import *
from donkeycar.parts.camera import CSICamera
from ai_drive_models import LinearModel, DriveClass, RNNModel
import random


class RandomActionGenerator:
    # used for inference, with the ai-drive-model packed.
    def __init__(self, min_throttle=-1.0, max_throttle=1.0, min_steering=-1.0, max_steering=1.0):
        self.min_throttle = min_throttle
        self.max_throttle = max_throttle
        self.min_steering = min_steering
        self.max_steering = max_steering

        self.steering = 0.0
        self.throttle = 0.0

    def update(self):
        # used for threaded version.
        while True:
            print('!!! action changing randomly !!!')
            random = random.random() # generate a random number in [0,1]
            self.steering = (self.max_steering - self.min_steering) * random + self.min_steering
            random = random.random()
            self.throttle = (self.max_throttle - self.min_throttle) * random + self.min_throttle
            print(' --> random action generator, steering = %.2f, throttle = %.2f'%(self.steering, self.throttle))
            time.sleep(5) # sleep for 5 seconds in this thread
    
    def run_threaded(self):
        # this method is called at a frame based on the RATE_HZ
        return self.steering, self.throttle


class BasicMotionController:       
    def run(self, steering, throttle):
        steering += 0.05
        throttle -= 0.05
        print(' --> motion controller, steering = %.2f, throttle = %.2f'%(steering, throttle))
        return steering, throttle

def drive(cfg):

    # -------------------------------- 
    # 1. Initialize car
    # --------------------------------
    V = dk.vehicle.Vehicle()

    # -------------------------------
    # 2. Add a Random Action Generator
    # -------------------------------
    random_action_generator = RandomActionGenerator(min_throttle=-0.7, max_throttle=0.7)
    V.add(random_action_generator, 
          inputs=[],
          outputs=['user/angle', 'user/throttle'],
          threaded=True)

    # -------------------------------
    # 3. Add a Basic Motion Controller to receive the random action generated above and do some modifications.
    # -------------------------------
    basic_motion_controller = BasicMotionController()
    V.add(basic_motion_controller, 
          inputs=['user/angle', 'user/throttle'],
          outputs=['angle', 'throttle'],
          threaded=False)

    # -------------------------------- 
    # 5. Configure the low-level controller that translates steering and throttle to PWM signals
    # -------------------------------- 
    steering_controller = PCA9685(cfg.STEERING_CHANNEL, cfg.PCA9685_I2C_ADDR, busnum=cfg.PCA9685_I2C_BUSNUM)
    steering = PWMSteering(controller=steering_controller,
                                    left_pulse=cfg.STEERING_LEFT_PWM,
                                    right_pulse=cfg.STEERING_RIGHT_PWM)

    throttle_controller = PCA9685(cfg.THROTTLE_CHANNEL, cfg.PCA9685_I2C_ADDR, busnum=cfg.PCA9685_I2C_BUSNUM)
    throttle = PWMThrottle(controller=throttle_controller,
                                    max_pulse=cfg.THROTTLE_FORWARD_PWM,
                                    zero_pulse=cfg.THROTTLE_STOPPED_PWM,
                                    min_pulse=cfg.THROTTLE_REVERSE_PWM)

    V.add(steering, inputs=['angle'], threaded=True)
    V.add(throttle, inputs=['throttle'], threaded=True)


    # -------------------------------- 
    # 6. run the vehicle for rate_hz, e.g., 20 HZ, here we set to 1 HZ for showing the printed info.
    # -------------------------------- 
    V.start(rate_hz=1, max_loop_count=None)


if __name__ == '__main__':
    cfg = dk.load_config()
    drive(cfg)
