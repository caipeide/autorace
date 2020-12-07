import serial  
import time
import struct


def get_pose(data): # m
    # ref: https://stackoverflow.com/questions/3783677/how-to-read-integers-from-a-file-that-are-24bit-and-little-endian-using-python
    # ref: https://www.cnblogs.com/litaozijin/p/6506354.html
    # ref: https://www.delftstack.com/zh/howto/python/how-to-convert-bytes-to-integers/#python-3-%25E4%25B8%25AD%25E7%259A%2584%25E5%25AD%2597%25E8%258A%2582-bytes
    temp = [0, 0, 0]
    MULTIPLY = 1.0/1000
    x = data[0: 3]
    y = data[3: 6]
    z = data[6: 9]
    temp[0] = int.from_bytes(x, byteorder='little', signed=True) * MULTIPLY
    temp[1] = int.from_bytes(y, byteorder='little', signed=True) * MULTIPLY
    temp[2] = int.from_bytes(z, byteorder='little', signed=True) * MULTIPLY
    
    return temp

def get_vel(data): # m/s
    temp = [0, 0, 0]
    MULTIPLY = 1.0/10000
    x = data[0: 3]
    y = data[3: 6]
    z = data[6: 9]
    temp[0] = int.from_bytes(x, byteorder='little', signed=True) * MULTIPLY
    temp[1] = int.from_bytes(y, byteorder='little', signed=True) * MULTIPLY
    temp[2] = int.from_bytes(z, byteorder='little', signed=True) * MULTIPLY
    # print(temp)
    return temp

def get_orientation(data): # degree
    temp = [0, 0, 0]
    MULTIPLY = 1.0/100
    x = data[0: 2]
    y = data[2: 4]
    z = data[4: 6]
    temp[0] = int.from_bytes(x, byteorder='little', signed=True) * MULTIPLY
    temp[1] = int.from_bytes(y, byteorder='little', signed=True) * MULTIPLY
    temp[2] = int.from_bytes(z, byteorder='little', signed=True) * MULTIPLY
    # print(temp)
    return temp

def get_pose_uncertainty(data): # m
    temp = [0, 0, 0]
    MULTIPLY = 1.0/100
    temp[0] = data[0] * MULTIPLY
    temp[1] = data[1] * MULTIPLY
    temp[2] = data[2] * MULTIPLY
    # print(temp)
    return temp

def get_voltage(data): # V
    temp = 0
    MULTIPLY = 1.0/1000
    temp = int.from_bytes(data, byteorder='little', signed=False) * MULTIPLY
    # print(temp)
    return temp

def get_imu(data):
    # angular_velcity: rad/s
    # acceleration: m/s^2
    temp = [0, 0, 0]
    x = data[0: 4]
    y = data[4: 8]
    z = data[8: 12]
    temp[0] = float(struct.unpack('<f', x)[0])
    temp[1] = float(struct.unpack('<f', y)[0])
    temp[2] = float(struct.unpack('<f', z)[0])
    # print(temp)
    return temp

def check(strr):
    # ref: https://my.oschina.net/u/4279343/blog/3331517
    summ = 0
    for i in range(127):
        summ += int(strr[i])	
    summ %= 256
    return summ == int(strr[127])


class UWBClass:
    def __init__(self, cfg, cam):
        self.cam = cam
        self.cfg = cfg
        # open the serial port
        print('opening the serial port: %s with baud rate: %d'%(cfg.SERIAL_PORT, cfg.BAUD_RATE))
        self.t = serial.Serial(cfg.SERIAL_PORT, cfg.BAUD_RATE, timeout=0.5)
        # define variables
        self.vel_x = 0
        self.vel_y = 0
        self.vel_z = 0

        self.acl_x = 0
        self.acl_y = 0
        self.acl_z = 0

        self.gyr_x = 0
        self.gyr_y = 0
        self.gyr_z = 0

        self.pose_x = 0
        self.pose_y = 0
        self.pose_z = 0

        self.ori_x = 0
        self.ori_y = 0
        self.ori_z = 0

        self.id = 100

        self.pose_unc_x = 0
        self.pose_unc_y = 0
        self.pose_unc_z = 0

        self.voltage = 0
        
    def update(self):
        data_buffer2 = bytes()
        while self.cam.running:
            data_hex = None
            final_data_hex = None

            time.sleep(0.002) # faster than 50 hz
            num = self.t.inWaiting()
            data_buffer1 = self.t.read(num)
            # print(len(data_buffer1), len(data_buffer2), data_buffer2[:2] == b'U\x01', end=' ')

            # 一级缓存
            if data_buffer1[:2] == b'U\x01': # start frame.

                if len(data_buffer1) == 128:
                    data_hex = data_buffer1
                    
                elif len(data_buffer1) > 128:
                    data_hex = data_buffer1[:128]
                    data_buffer2 = data_buffer1[128:]

                elif len(data_buffer1) < 128:
                    data_buffer2 = data_buffer1
            else:
                data_buffer2 += data_buffer1
                
            # 二级缓存
            if data_buffer2[:2] == b'U\x01':

                if len(data_buffer2) > 128:
                    data_buffer2 = data_buffer2[:128]
                
                if len(data_buffer2) == 128:
                    data_hex = data_buffer2
                    data_buffer2 = bytes() # 清空缓存
            
            # check sum
            if data_hex:
                if check(data_hex):
                    final_data_hex = data_hex
                    # print('SUCCESS', end= ' ')
            
            # get info
            if final_data_hex:
                self.id = int(final_data_hex[2])
                self.pose_x, self.pose_y, self.pose_z = get_pose(final_data_hex[4:13])
                self.vel_x, self.vel_y, self.vel_z = get_vel(final_data_hex[13:22])
                self.gyr_x, self.gyr_y, self.gyr_z = get_imu(final_data_hex[46:58])
                self.acl_x, self.acl_y, self.acl_z = get_imu(final_data_hex[58:70])
                self.ori_x, self.ori_y, self.ori_z = get_orientation(final_data_hex[82:88])
                self.pose_unc_x, self.pose_unc_y, self.pose_unc_z = get_pose_uncertainty(final_data_hex[117:120])
                self.voltage = get_voltage(final_data_hex[120:122])
                # print(self.voltage)
            
        print('closing the serial port of UWB system: ', self.cfg.SERIAL_PORT)
        serial.Serial.close(self.t)
            
    def run_threaded(self):
        return self.acl_x, self.acl_y, self.acl_z, self.gyr_x, self.gyr_y, self.gyr_z, self.vel_x, self.vel_y, self.vel_z, self.pose_x, self.pose_y, self.pose_z, self.pose_unc_x, self.pose_unc_y, self.pose_unc_z, self.ori_x, self.ori_y, self.ori_z, self.id, self.voltage