# FEI NGIO UI V2

## Environment Setup

#### Create a virtual environment - Windows
* First make sure you have python installed, ideally from python.org, and installed on your PATH
* Open the Folder in VS code containing the python code with *main.py* at the root level.
* On Windows, run in terminal **python -m venv ./venv**  You should see a venv folder appear in your source directory.
* To activate the venv, run **venv/Scripts/activate**
* Once this is activated (you should see (venv) in front of your command line), install the python dependencies
* **pip install -r requirements.txt** from the root directory should install all required pip libraries

#### Create a virtual environment - Linux
* First make sure you have python installed, if not you can run *sudo apt-get install python* from a terminal to install.
* you can also install VS code with **sudo apt-get install code** on linux.
* Open the Folder in vs code containing the python code with *main.py* at the root level.
* On Windows, run in terminal **python -m venv ./venv** You should see a venv folder appear in your source directory.
* To activate the venv, run **venv/bin/activate** NOTE THE DIFFERENCE FROM WINDOWS
* Once this is activated (you should see (venv) in front of your command line), install the python dependencies
* **pip install -r requirements.txt** from the root directory should install all required pip libraries

## Usage

#### Select your EtherCAT Network Adapter
* Look at line 17-18 in ethercat.py and make sure the adapter_name matches the adapter you are using.
* To determine your adapter name, run the file find_adapters.py, which will print out all your network adapters ID's
* If you are on a Raspberry Pi or linux, the adapter should be as simple as 'eth0'
* It is a little more complicated on windows, the adapter format should be similar to : '\Device\NPF_{DEADBEEF-DEAD-BEEF-DEAD-BEEEEEEEEF}'
* *Make sure to format your string with double backslashes in python*
* Simply use that string as the adapter name in fei_ethercat, and you should be good to go.

#### Starting the UI
* To start the UI, run *main.py*
* If you receive an error, make sure the board is powered up and the ethernet cable is plugged into the correct port(bottom)
* The program will parse Config_sheet.xlsx and configure connected slot boards based on the specified type in the excel

* As of 10/17/23 the ui callbacks have yet to be implemented