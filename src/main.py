# Author: Sai Shankar
# TID: T0159ZN
# Date: 2024-03-17
# Title: BCA-BSW IOHWAB Test Automation Framework
# Description: A comprehensive framework designed to streamline the BCA-BSW IOHwAb testing process, making it more efficient and effective.

import time, getpass, datetime, os, configparser
import pandas as pd
from sensor_numato_relay_module import relay_serial_port
from actuator_mcu_module import mcu_serial_port
from html_report import html_report_generator

class Test_Automation_Framework_for_IOHwAb:
    def __init__(self, mcu_port_name: str, numato_usb_relay_port_name: str):
        # H7 Micro Controller Unit COM port
        self.mcu_port:str = mcu_port_name

        # Numato USB Relay COM port
        self.numato_usb_relay_port:str = numato_usb_relay_port_name

        self.ian_relay_config_file_path = os.path.join(os.path.dirname(__file__), '../config/ian_relay.config')

        # Report Data
        self.report_data:dict = {}
        self.report_data['user'] = getpass.getuser()
        self.report_data['test_begin_time'] = datetime.datetime.now()
        self.report_data['overall_result'] = False
        self.report_data['total_testcases'] = 0
        self.report_data['testcases_executed'] = 0
        self.report_data['testcases_not_executed'] = 0
        self.report_data['testcases_passed'] = 0
        self.report_data['testcases_failed'] = 0

        # Testcases status list
        self.testcases_list:list = []

    def config_parser(self, section:str, option:str) -> tuple[str, str]:
        config = configparser.ConfigParser()
        with open(self.ian_relay_config_file_path, '+r') as file:
            filestr = file.read()

        config.read_string(filestr)

        value = config.get(section, option)
        return option, value

    def mcu_module(self)-> None:
        # Instance of MCU
        # Parameters : (MCU COM port Name)
        self.mcu_serial_port = mcu_serial_port(self.mcu_port)

        # Connecting of MCU
        self.mcu_serial_port.open()

        # MCU reset
        self.mcu_serial_port.reset()
        time.sleep(5)

        # MCU panel refresh
        self.mcu_serial_port.refresh('Refresh1')

    def test_setup(self)-> None:
        self.report_data['test_setup'] = {
            'step1': False,
            'step2': False,
        }

        #######################################################################################################################
        # Connecting COM port of Numato USB Relaycard
        print(f"\n\nConnect the {self.numato_usb_relay_port} port of Numato USB Relay")
        # Instance of Numato USB Relay module
        # Parameters : (USB Relay COM port Name)
        self.numato_usb_relay_serial_port = relay_serial_port(self.numato_usb_relay_port)
        # Connecting to USB Relay COM Port
        self.numato_usb_relay_serial_port.open()
        # USB Relaycard version
        self.numato_usb_relay_serial_port.version()

        self.report_data['test_setup']['step1'] = True
        #######################################################################################################################

        #######################################################################################################################
        # connecting COM port of MCU, MCU panel reset and MCU refresh
        print(f"\n\nConnect the {self.mcu_port} port to the Test Framework")
        # Instance of MCU
        # Parameters : (MCU COM port Name)
        self.mcu_serial_port = mcu_serial_port(self.mcu_port)

        # Connecting of MCU
        self.mcu_serial_port.open()
        time.sleep(1)
        # MCU reset
        self.mcu_serial_port.reset()

        # MCU panel refresh
        # self.mcu_serial_port.refresh('Refresh1')
        # time.sleep(5)
        self.report_data['test_setup']['step2'] = True
        #######################################################################################################################

    def test_setup_teardown(self)-> None:
        self.report_data['test_setup_teardown'] = {
            'step1': False,
            'step2': False,
        }

        # Disconnecting Numato Relay Serial COM port
        print("Disconnecting Numato Relay Serial COM port")
        self.numato_usb_relay_serial_port.close()
        self.report_data['test_setup_teardown']['step1'] = True

        # Disconnecting MCU Serial COM port
        self.mcu_serial_port.close()
        self.report_data['test_setup_teardown']['step2'] = True

    def testcase(self, Zone:str, RQM_ID:str, Testcase_Name:str, Testcase_Description:str, IAN_No:str=None, ODH_Pin:str=None)->list:
        self.report_data['testcases'][Testcase_Name] = {
            'rqm_id': RQM_ID,
            'testcase_description': Testcase_Description,
            'testcase_name': Testcase_Name,
            'ODH_Pin': ODH_Pin,
            'result': False,
            'Zone': Zone,
        }

        print(f"\nTestcase of {RQM_ID} - {Testcase_Name}")

        if IAN_No!='No':
            self.report_data['testcases'][Testcase_Name]['IAN_No'] = IAN_No
            IAN, channels = self.config_parser('IAN_Source', IAN_No)

            channels:list[str] = channels.split(',')
            
            if len(channels)==2:
                for channel in channels:
                    self.numato_usb_relay_serial_port.relay_on(channel)
                time.sleep(5)
                self.ol:list = self.mcu_serial_port.refresh_all()
                # time.sleep(5)
                # self.ol:list = self.mcu_serial_port.refresh_all()

                print(self.ol)

        status:bool = None
        if ODH_Pin in self.ol:
            #print("Digital output is verified")
            print(f'{Testcase_Name},{ODH_Pin} pin status is HIGH')
            print("Testcase passed")
            self.report_data['testcases'][Testcase_Name]['result'] = True
            status = True
        else:
            #print("Digital output is not verified")
            print(f'{Testcase_Name},{ODH_Pin} pin status is LOW')
            print("Testcase failed")
            self.report_data['testcases'][Testcase_Name]['result']= False
            status = False
        
        if IAN_No!='No' and len(channels)==2:
            for channel in channels:
                self.numato_usb_relay_serial_port.relay_off(channel)
        
        return [Testcase_Name, status]

    def testcases(self):
        self.report_data['testcases'] = {}
        results_csv_path = os.path.join(os.path.dirname(__file__), '../inputs/sensor_actuator_testcases_data.csv')
        df = pd.read_csv(results_csv_path)

        grouped_df = df.sort_values(by='Test_type')
        df = grouped_df.reset_index(drop=True)
        # print(df.head())
        
        self.ol:list = self.mcu_serial_port.refresh_all()
        print('Pins On:', self.ol)
        for index, row in df.iterrows():
            zone:str = row['Variant']
            test_type:str = row['Test_type']
            rqm_id:str = row['TC_RQM_ID']
            testcase_name:str = row['Tescase Name']
            testcase_description:str = f'To verify the {testcase_name} {test_type}  Hardware Pin status in {zone}'
            ian_no:str = row['IAN_No']
            out_pin:str = row['ODH_No']

            if test_type == 'Actuator' or test_type == 'Sensor&Actuator':
                self.testcase(zone, rqm_id, testcase_name, testcase_description, ian_no, out_pin)
        
        for key, value in self.report_data['testcases'].items():
            self.report_data['total_testcases']+=1
            if value['result']:
                self.report_data['testcases_passed']+=1
            else:
                self.report_data['testcases_failed']+=1

        if self.report_data['testcases_passed'] == self.report_data['total_testcases']:
            self.report_data['overall_result'] = True

    def main(self):
        try:
            print('\n\nStep-1: Test Setup Initialization')
            self.test_setup()

            # Execution of Testcases
            print('\n\nStep-2: Test Case Run')
            self.testcases()

            print("\n\nStep-3: Testcase Setup TearDown")
            self.test_setup_teardown()

            self.report_data['test_end_time'] = datetime.datetime.now()

            # Generating html repot
            r = html_report_generator(self.report_data)
            r.generate_report()
        except Exception as e:
            self.test_setup_teardown()
            print('Error', e)


# BCA-BSW IOHWAB Automation Test Framework
# Test_automation_framework_for_IOHwAb Instance
# Parameters : (COM Port of USB Relay,  COM Port of IMON Test Hardware)
print("*"*10,"BCA-BSW IOHWAB Automation Testing Framework", "*"*10)
taf = Test_Automation_Framework_for_IOHwAb(mcu_port_name="COM5", numato_usb_relay_port_name="COM4")
taf.main()