# """
# CAR CONFIG

# This file is read by your car application's manage.py script to change the car
# performance.

# EXMAPLE
# -----------
# import dk
# cfg = dk.load_config(config_path='~/mycar/config.py')
# print(cfg.CAMERA_RESOLUTION)

# """

# import os

# #PATHS
# CAR_PATH = PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
# DATA_PATH = os.path.join(CAR_PATH, 'data')
# MODELS_PATH = os.path.join(CAR_PATH, 'models')

# #VEHICLE
# DRIVE_LOOP_HZ = 10      # the vehicle loop will pause if faster than this speed.
# MAX_LOOPS = None        # the vehicle loop can abort after this many iterations, when given a positive integer.

# #CAMERA
# CAMERA_TYPE = "CSIC"   # (PICAM|WEBCAM|CVCAM|CSIC|V4L|D435|MOCK|IMAGE_LIST), We use CSIC in this competition.
# IMAGE_W = 224
# IMAGE_H = 224
# IMAGE_DEPTH = 3         # default RGB=3, make 1 for mono
# CAMERA_FRAMERATE = DRIVE_LOOP_HZ

#UWB
# HAVE_UWB = True
# SERIAL_PORT = '/dev/ttyUSB0'
# BAUD_RATE = 921600

# # Region of interst cropping
ROI_CROP_TOP = 35                    #the number of rows of pixels to ignore on the top of the image
ROI_CROP_BOTTOM = 10                 #the number of rows of pixels to ignore on the bottom of the image

# #9865, over rides only if needed, ie. TX2..
# PCA9685_I2C_ADDR = 0x40     #I2C address, use i2cdetect to validate this number
# PCA9685_I2C_BUSNUM = 1   #None will auto detect, which is fine on the pi. But other platforms should specify the bus num.

# #STEERING
# STEERING_CHANNEL = 0            #channel on the 9685 pwm board 0-15
STEERING_LEFT_PWM = 460         #pwm value for full left steering
STEERING_RIGHT_PWM = 290        #pwm value for full right steering

# #STEERING FOR PIGPIO_PWM
# STEERING_PWM_PIN = 13           #Pin numbering according to Broadcom numbers
# STEERING_PWM_FREQ = 50          #Frequency for PWM
# STEERING_PWM_INVERTED = False   #If PWM needs to be inverted

# #THROTTLE FOR PIGPIO_PWM
# THROTTLE_PWM_PIN = 18           #Pin numbering according to Broadcom numbers
# THROTTLE_PWM_FREQ = 50          #Frequency for PWM
# THROTTLE_PWM_INVERTED = False   #If PWM needs to be inverted


# #TRAINING
# #The DEFAULT_MODEL_TYPE will choose which model will be created at training time. This chooses
# #between different neural network designs. You can override this setting by passing the command
# #line parameter --type to the python manage.py train and drive commands.
# DEFAULT_MODEL_TYPE = 'linear'   #(linear|categorical|rnn|imu|behavior|3d|localizer|latent)
# BATCH_SIZE = 128                #how many records to use when doing one pass of gradient decent. Use a smaller number if your gpu is running out of memory.
# TRAIN_TEST_SPLIT = 0.8          #what percent of records to use for training. the remaining used for validation.
# MAX_EPOCHS = 100                #how many times to visit all records of your data
# EARLY_STOP_PATIENCE = 5         #how many epochs to wait before no improvement
# MIN_DELTA = .0005               #early stop will want this much loss change before calling it improved.
# PRINT_MODEL_SUMMARY = True      #print layers and weights to stdout
# LEARNING_RATE = 0.0001           #only used when OPTIMIZER specified
# NUM_WORKERS = 8                 # Setting the argument num_workers as a positive integer will turn on multi-process data loading with the specified number of loader worker processes.
# COLOR_JITTER_TRANSFORMS = True  #weather to add color noise (brightness, contrast, ...) during training.

# #WEB CONTROL
# WEB_CONTROL_PORT = 8887             # which port to listen on when making a web controller
# WEB_INIT_MODE = "user"              # which control mode to start in. one of user|local_angle|local. Setting local will start in ai mode.

# #JOYSTICK
# USE_JOYSTICK_AS_DEFAULT = False     #when starting the manage.py, when True, will not require a --js option to use the joystick
JOYSTICK_MAX_THROTTLE = 0.5         # [0,1], this scalar is multiplied with the throttle value (-1 to 1) to limit the maximum throttle. This can help if you drop the controller or just don't need the full speed available.
# JOYSTICK_STEERING_SCALE = 1.0       #some people want a steering that is less sensitve. This scalar is multiplied with the steering -1 to 1. It can be negative to reverse dir.
# AUTO_RECORD_ON_THROTTLE = True      #if true, we will record whenever throttle is not zero. if false, you must manually toggle recording with some other trigger. Usually circle button on joystick.
# JOYSTICK_DEADZONE = 0.0             # when non zero, this is the smallest throttle before recording triggered.
# JOYSTICK_THROTTLE_DIR = -1.0        # use -1.0 to flip forward/backward, use 1.0 to use joystick's natural forward/backward
# USE_FPV = False                     # send camera data to FPV webserver
# JOYSTICK_DEVICE_FILE = "/dev/input/js0" # this is the unix file use to access the joystick.
GENTLE_THROTTLE = 0.5
RAGE_THROTTLE = 0.7
PER_THROTTLE_STEP = 0.05

# #RNN or 3D
# SEQUENCE_LENGTH = 3             #some models use a number of images over time. This controls how many.

# #RECORD OPTIONS
RECORD_DURING_AI = True        #normally we do not record during ai mode. Set this to true to get image and steering records for your Ai. Be careful not to use them to train.

# #Scale the output of the throttle of the ai pilot for all model types.
# AI_THROTTLE_MULT = 1.0              # this multiplier will scale every throttle value for all output from NN models

# Whether or not add extra control noise during user mode
CONTROL_NOISE = True