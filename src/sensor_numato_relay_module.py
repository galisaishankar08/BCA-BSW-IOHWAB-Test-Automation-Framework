# Author: Sai Shankar
# TID: T0159ZN
# Date: 2024-03-17
# Description: Numato 16 Channel Relay module all command functions for Sensor testing

import serial

class relay_serial_port:
    def __init__(self, port:str):
        self.ser = serial.Serial()
        self.port:str = port

    def open(self):
        self.ser.port = self.port
        self.ser.baudrate = 9600
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 0.5
        self.ser.write_timeout = 0.5
        if not self.ser.is_open:
            self.ser.open()
        print('Connected to', self.port ,'port')

    def relay_status(self, relay_Num:str)->bool:
        if (int(relay_Num) < 10):
            relayIndex:str = str(relay_Num)
        else:
            relayIndex:str = chr(55 + int(relay_Num))
            
        self.ser.write(("relay read "+ relayIndex + "\n\r").encode('utf_8'))

        response = self.ser.read(25).decode()
        # print('Hi',response)

        if(response.find("on") > 0):
            return True
        elif(response.find("off") > 0):
            return False

    def relay_on(self, relay_Num:str)->bool:
        try:
            if (int(relay_Num) < 10):
                relayIndex:str = str(relay_Num)
            else:
                relayIndex:str = chr(55 + int(relay_Num))
                
            self.ser.write(("relay on "+ relayIndex + "\n\r").encode('utf_8'))
            
            if self.relay_status(relay_Num):
                print("Relay " + str(relay_Num) +" is ON")
                return True
            print("Error: Relay " + str(relay_Num) +" is OFF")
            return False
        except Exception as e:
            print(e)
            return False

    def relay_off(self, relay_Num):
        try:
            if (int(relay_Num) < 10):
                relayIndex:str = str(relay_Num)
            else:
                relayIndex:str = chr(55 + int(relay_Num))
            self.ser.write(("\n\rrelay off "+ relayIndex + "\n\r").encode('utf_8'))
            
            if not self.relay_status(relay_Num):
                print("Relay " + str(relay_Num) +" is OFF")
                return True
            return False
        except Exception as e:
            print(e)
            return False

    def version(self)->None:
        self.ser.write(("\n\rver \n\r").encode('utf_8'))
        res:str = self.ser.read(25).decode()
        print(res)

    def read_all(self)->None:
        self.ser.write(("\n\rrelay readall \n\r").encode('utf_8'))
        res:str = self.ser.read(25).decode()
        print(res)  

    def write_all(self)->None:
        self.ser.write(("\n\rrelay writeall ffff \n\r").encode('utf_8'))
        res:str = self.ser.read(25).decode()
        print(res)    

    def close(self)->None:
        self.ser.close()
        print('closed', self.port, 'port')