import binascii
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

def hexShow(argv):        #十六进制显示 方法1
    try:
        result = ''  
        hLen = len(argv)
        # print(hLen)
        for i in range(hLen):  
         hvol = argv[i]
         hhex = '%02x'%hvol  
         result += hhex+' '  
        # print('hexShow:',result)
        # print()
        return result
    except:
        pass

t = serial.Serial('/dev/tty.usbserial-14310',921600,timeout=0.5)
data_buffer2 = bytes()
while True:
    data_string = None
    data_hex = None
    final_data_hex = None

    time.sleep(0.002) # faster than 50 hz
    num = t.inWaiting()
    data_buffer1 = t.read(num)
    print(len(data_buffer1), len(data_buffer2), data_buffer2[:2] == b'U\x01', end=' ')

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
            print('SUCCESS', end= ' ')
    
    # get info
    if final_data_hex:
        print("ID: ",int(final_data_hex[2]), end=' | ')
        print("ROLE_NUM: ",int(final_data_hex[3]), end=' | ')
        print("POSE: ",get_pose(final_data_hex[4:13]), end='')
        print("VEL: ", get_vel(final_data_hex[13:22]), end='')
        print("ANG VEL: ", get_imu(final_data_hex[46:58]), end='')
        print("ACCEL: ", get_imu(final_data_hex[58:70]), end='')
        print("ORIEN: ", get_orientation(final_data_hex[82:88]), end='')
        print("POSE_UNCERT: ", get_pose_uncertainty(final_data_hex[117:120]), end='')
        print("VOLTAGE: ", get_voltage(final_data_hex[120:122]), end='')
    
    print()

serial.Serial.close(t)