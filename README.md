# MI Scale 2 Python script
Python script to read values from MI Scale 2. Under testing. Test and report if the script returns correct (or nearly correct) data or not.
Add required details like your MI Scale MAC address, MQTT username, password, host IP address in the code.
You also need to add your height in cm in the code to calculate BMI and other data which depends upon it.
Calculation formulas taken from openScale page. (https://github.com/oliexdev/openScale/)




## Setup on Raspberry Pi 3

### Install dependencies

    apt-get install python3-pip libglib2.0-dev
    pip3 install bluepy

### find mac of Scale 

    hcitool -i hci0 lescan
 
### Run script

Insert mac to python script & Run
