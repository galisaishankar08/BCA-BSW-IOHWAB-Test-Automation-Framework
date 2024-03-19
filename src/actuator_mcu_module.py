# Author: Sai Shankar
# TID: T0159ZN
# Date: 2024-03-17
# Description: Tester Board MCU module all required commands functions for Actuator testing

import serial, time, re, configparser, os

class mcu_serial_port:
    def __init__(self, port:str):
        self.ser = serial.Serial()
        self.port:str = port

    def open(self):
        self.ser.port = self.port
        self.ser.baudrate = 115200
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 0.5
        self.ser.write_timeout = 0.5
        if not self.ser.is_open:
            self.ser.open()
        print('Connected to', self.port ,'port')
        

    def reset(self)->None:
        self.ser.write(("RESET\n\r").encode('utf_8'))
        self.ser.write(("RESET\n\r").encode('utf_8'))
        time.sleep(2)
        message = self.ser.read_until('\n\r').decode()
        if message:
            print(message)
            time.sleep(10)

    def refresh(self, cmd)->list:
        self.ser.write((cmd+"\n\r").encode('utf_8'))
        self.ser.write((cmd+"\n\r").encode('utf_8'))
        time.sleep(5)

        message:str = self.ser.read_until('\n\r').decode()
        if not message:
            self.ser.write((cmd+"\n\r").encode('utf_8'))
            self.ser.write((cmd+"\n\r").encode('utf_8'))
            message:str = self.ser.read_until('\n\r').decode()

        messages:list = message.split('\n\r')

        print(cmd, 'Messages: ', messages, '\n')
        return messages

    def config_parser(self, config_path:str, section:str, option:str)-> tuple[str, str]:
        config = configparser.ConfigParser()
        with open(config_path, '+r') as file:
            filestr:str = file.read()

        config.read_string(filestr)

        value:str = config.get(section, option)
        return option, value

    def refresh_all(self):
        all_messages:list = []

        r1:list = self.refresh('Refresh1')
        all_messages += r1
        time.sleep(3)

        unq_messages:dict = {}
        for msg in all_messages:
            match = re.search(r"IO_[0-9]=(\d{4})#", msg)
            if match:
                unq_messages[match.group(0)[0:4]] = match.group(1)

        # print(unq_messages)
        ol:list = []
        out_config_file_path:str = os.path.join(os.path.dirname(__file__), '../config/pin_odh.config')

        if unq_messages.get('IO_1'):
            output:str = unq_messages.get('IO_1')

            binary_value = bin(int(output, 16))[2:]
            full_binary_value = binary_value.zfill(16)[::-1]

            for i in range(len(full_binary_value)):
                if full_binary_value[i]=="1":
                    # print(output[i+1+16], "is ON")
                    key, out = self.config_parser(out_config_file_path, '0x40', 'P'+str(i))
                    ol.append(out)
                    # print(out)
                # else:
                #     print(output[i+1+16], "is OFF")

        return ol

    def close(self)->None:
        self.ser.close()
        print('closed', self.port, 'port')