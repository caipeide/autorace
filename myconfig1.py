"""
CAR CONFIG

This file is read by your car application's manage.py script to change the car
performance.

EXMAPLE
-----------
import dk
cfg = dk.load_config(config_path='~/mycar/config.py')
print(cfg.CAMERA_RESOLUTION)

"""


import os

#PATHS
CAR_PATH = PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(CAR_PATH, 'data')
MODELS_PATH = os.path.join(CAR_PATH, 'models')

#VEHICLE
DRIVE_LOOP_HZ = 10      # the vehicle loop will pause if faster than this speed.
MAX_LOOPS = None        # the vehicle loop can abort after this many iterations, when given a positive integer.

#CAMERA
CAMERA_TYPE = "CSIC"   # (PICAM|WEBCAM|CVCAM|CSIC|V4L|D435|MOCK|IMAGE_LIST), We use CSIC in this competition.
IMAGE_W = 224
IMAGE_H = 224
IMAGE_DEPTH = 3         # default RGB=3, make 1 for mono
CAMERA_FRAMERATE = DRIVE_LOOP_HZ
CAMERA_VFLIP = False
CAMERA_HFLIP = False
# For CSIC camera - If the camera is mounted in a rotated position, changing the below parameter will correct the output frame orientation
CSIC_CAM_GSTREAMER_FLIP_PARM = 0 # (0 => none , 4 => Flip horizontally, 6 => Flip vertically)

#9865, over rides only if needed, ie. TX2..
PCA9685_I2C_ADDR = 0x40     #I2C address, use i2cdetect to validate this number
PCA9685_I2C_BUSNUM = 1   #None will auto detect, which is fine on the pi. But other platforms should specify the bus num.

#STEERING
STEERING_CHANNEL = 0            #channel on the 9685 pwm board 0-15
STEERING_LEFT_PWM = 460         #pwm value for full left steering
STEERING_RIGHT_PWM = 265        #pwm value for full right steering

#STEERING FOR PIGPIO_PWM
STEERING_PWM_PIN = 13           #Pin numbering according to Broadcom numbers
STEERING_PWM_FREQ = 50          #Frequency for PWM
STEERING_PWM_INVERTED = False   #If PWM needs to be inverted

#THROTTLE
THROTTLE_CHANNEL = 1            #channel on the 9685 pwm board 0-15
THROTTLE_FORWARD_PWM = 440      #500, pwm value for max forward throttle 460
THROTTLE_STOPPED_PWM = 390      #pwm value for no movement
THROTTLE_REVERSE_PWM = 300      #220, pwm value for max reverse throttle

#THROTTLE FOR PIGPIO_PWM
THROTTLE_PWM_PIN = 18           #Pin numbering according to Broadcom numbers
THROTTLE_PWM_FREQ = 50          #Frequency for PWM
THROTTLE_PWM_INVERTED = False   #If PWM needs to be inverted


#TRAINING
#The DEFAULT_MODEL_TYPE will choose which model will be created at training time. This chooses
#between different neural network designs. You can override this setting by passing the command
#line parameter --type to the python manage.py train and drive commands.
DEFAULT_MODEL_TYPE = 'linear'   #(linear|categorical|rnn|imu|behavior|3d|localizer|latent)
BATCH_SIZE = 128                #how many records to use when doing one pass of gradient decent. Use a smaller number if your gpu is running out of memory.
TRAIN_TEST_SPLIT = 0.8          #what percent of records to use for training. the remaining used for validation.
MAX_EPOCHS = 100                #how many times to visit all records of your data
SHOW_PLOT = True                #would you like to see a pop up display of final loss?
VERBOSE_TRAIN = True             #would you like to see a progress bar with text during training?
USE_EARLY_STOP = True           #would you like to stop the training if we see it's not improving fit?
EARLY_STOP_PATIENCE = 5         #how many epochs to wait before no improvement
MIN_DELTA = .0005               #early stop will want this much loss change before calling it improved.
PRINT_MODEL_SUMMARY = True      #print layers and weights to stdout
OPTIMIZER = None                #adam, sgd, rmsprop, etc.. None accepts default
LEARNING_RATE = 0.0001           #only used when OPTIMIZER specified
LEARNING_RATE_DECAY = 0.0       #only used when OPTIMIZER specified
SEND_BEST_MODEL_TO_PI = False   #change to true to automatically send best model during training
CACHE_IMAGES = True             #keep images in memory. will speed succesive epochs, but crater if not enough mem.

# PRUNE_CNN = False               #This will remove weights from your model. The primary goal is to increase performance.
# PRUNE_PERCENT_TARGET = 75       # The desired percentage of pruning.
# PRUNE_PERCENT_PER_ITERATION = 20 # Percenge of pruning that is perform per iteration.
# PRUNE_VAL_LOSS_DEGRADATION_LIMIT = 0.2 # The max amout of validation loss that is permitted during pruning.
# PRUNE_EVAL_PERCENT_OF_DATASET = .05  # percent of dataset used to perform evaluation of model.

# Region of interst cropping
# only supported in Categorical and Linear models.
# If these crops values are too large, they will cause the stride values to become negative and the model with not be valid.
ROI_CROP_TOP = 0                    #the number of rows of pixels to ignore on the top of the image
ROI_CROP_BOTTOM = 0                 #the number of rows of pixels to ignore on the bottom of the image

#WEB CONTROL
WEB_CONTROL_PORT = 8887             # which port to listen on when making a web controller
WEB_INIT_MODE = "user"              # which control mode to start in. one of user|local_angle|local. Setting local will start in ai mode.

#JOYSTICK
USE_JOYSTICK_AS_DEFAULT = False     #when starting the manage.py, when True, will not require a --js option to use the joystick
JOYSTICK_MAX_THROTTLE = 0.5         #this scalar is multiplied with the -1 to 1 throttle value to limit the maximum throttle. This can help if you drop the controller or just don't need the full speed available.
JOYSTICK_STEERING_SCALE = 1.0       #some people want a steering that is less sensitve. This scalar is multiplied with the steering -1 to 1. It can be negative to reverse dir.
AUTO_RECORD_ON_THROTTLE = True      #if true, we will record whenever throttle is not zero. if false, you must manually toggle recording with some other trigger. Usually circle button on joystick.
CONTROLLER_TYPE='xbox'               #(ps3|ps4|xbox|nimbus|wiiu|F710|rc3|MM1|custom) custom will run the my_joystick.py controller written by the `donkey createjs` command
USE_NETWORKED_JS = False            #should we listen for remote joystick control over the network?
NETWORK_JS_SERVER_IP = "192.168.0.1"#when listening for network joystick control, which ip is serving this information
JOYSTICK_DEADZONE = 0.0             # when non zero, this is the smallest throttle before recording triggered.
JOYSTICK_THROTTLE_DIR = -1.0        # use -1.0 to flip forward/backward, use 1.0 to use joystick's natural forward/backward
USE_FPV = True                     # send camera data to FPV webserver
JOYSTICK_DEVICE_FILE = "/dev/input/js0" # this is the unix file use to access the joystick.
GENTLE_THROTTLE = 0.45
RAGE_THROTTLE = 0.75
PER_THROTTLE_STEP = 0.05

#RNN or 3D
SEQUENCE_LENGTH = 3             #some models use a number of images over time. This controls how many.

#RECORD OPTIONS
RECORD_DURING_AI = False        #normally we do not record during ai mode. Set this to true to get image and steering records for your Ai. Be careful not to use them to train.


#publish camera over network
#This is used to create a tcp service to pushlish the camera feed
PUB_CAMERA_IMAGES = False

#Scale the output of the throttle of the ai pilot for all model types.
AI_THROTTLE_MULT = 1.0              # this multiplier will scale every throttle value for all output from NN models