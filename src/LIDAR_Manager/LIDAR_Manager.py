import serial
import time


class LIDAR_Manager:

    CMD_LASER_ON = bytes([0xCD, 0x01, 0x03, 0x04])
    CMD_LASER_OFF = bytes([0xCD, 0x01, 0x04, 0x05])
    CMD_MEASURE_B = bytes([0xCD, 0x01, 0x06, 0x07])

    def __init__(self,serial_port,baud_rate=115200,trigger_distance=3000):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.trigger_distance = trigger_distance
        self.ser = None

    def calibrate(self, samples=11, error_in_mm=300):
        values = []
        for _ in range(samples):
            distance = self.read_distance()
            if distance is not None:
                values.append(distance)
            if len(values) < 3:
                print("not enough values")
                return False
            values.sort()
            self.trigger_distance = values[len(values) // 2] - error_in_mm
            print("trigger distance:",self.trigger_distance,"mm")
            return True

    def start(self):
        self.ser = serial.Serial(self.serial_port,self.baud_rate,timeout=1)
        time.sleep(1)
        self.ser.reset_input_buffer()
        self.ser.write(self.CMD_LASER_ON)
        print(f"Lidar started: {self.serial_port}")

    def stop(self):
        if self.ser is not None:
            self.ser.write(self.CMD_LASER_OFF)
            self.ser.close()
            print(f"Lidar stopped: {self.serial_port}")
    def read_distance(self):
        try:
            time.sleep(1)
            self.ser.reset_input_buffer()
            self.ser.write(self.CMD_MEASURE_B)
            time.sleep(1)
            if self.ser.in_waiting <= 0:
                return None
            raw_data = self.ser.read(self.ser.in_waiting)
            if len(raw_data) < 8:
                return None
            header = raw_data[0]
            if header != 0xFA:
                return None
            expected_checksum = (sum(raw_data[1:7]) & 0xFF)
            received_checksum = raw_data[7]
            if expected_checksum != received_checksum:
                return None
            distance_low = raw_data[3]
            distance_high = raw_data[4]
            distance_mm = (distance_high << 8) | distance_low
            return distance_mm

        except Exception as e:
            print(f"Lidar Error: {e}")

        return None
    def vehicle_present(self):
        distance = self.read_distance()
        if distance is None:
            return False
        return distance < self.trigger_distance