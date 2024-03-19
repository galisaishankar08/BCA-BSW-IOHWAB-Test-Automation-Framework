# BCA-BSW-IOHWAB-Test-Automation-Framework

A comprehensive framework designed to streamline the BCA-BSW IOHwAb testing process, making it more efficient and effective.
 
## Author
 
**Gali Sai Shankar**
 
- GitHub: [@galisaishankar08](https://github.psa-cloud.com/galisaishankar08)
- LinkedIn: [GaliSaiShankar](https://www.linkedin.com/in/galisaishankar/)

**Mohammed Tajbaba**
 
## About The Project
**BCA-Sensor Actuator and BSW IOHwAb Automation Testing with Below Framework which contains the Tester Board ,USB Relay Board and ECU Board for BCA – BSW END to END Testing.**

Test framework is  used to communicate with UART Protocol to Monitor ,control and operate the Real time write/read of Actuator, IO and Sensor Signal Voltages Values on the different ECU  with the help of Tester Board and USB digital Relay card.​

* ECU Test Board is verified with help of Tester Board and USB Relay Board using the Test framework.​

* Tester Board communicates with UART Protocol with Test Bench PC using pyserial Framework to control  and monitor the ECU Board HW PIN status.​

* USB Relay Board communicates with UART Protocol with Test Bench PC using pyserial Framework to control write and read the ECU Board HW PIN status.​

* Report Generation: Test case Setup and Test case Run Steps

![Framework Workflow](https://github.com/galisaishankar08/BCA-BSW-IOHWAB-Test-Automation-Framework/assets/80621346/fbe59efb-f37b-495b-9bc0-f90b7d95b88b)
 
## Getting Started
 
* Clone Repository
```
git clone https://github.com/galisaishankar08/BCA-BSW-IOHWAB-Test-Automation-Framework.git
```
 
### Prerequisites
 
* Create Python Virtual Environment
```
python -m venv env 
```

* Activate Python Virtual Environment
```
.\env\Scripts\activate
```
 
### Installation
 
* Install Requirements
```
pip install -r requirements.txt
```

 
## Usage

* Run Framework
```
python .\src\main.py
```
