# FEI NGIO UI V2

## Environment Setup

#### Create a virtual environment - Windows
* First make sure you have python installed, ideally from python.org, and installed on your PATH
* Open the Folder in VS code containing the python code with *main.py* at the root level.
* On Windows, run in terminal **python -m venv ./venv**  You should see a venv folder appear in your source directory.
* To activate the venv, run **venv/Scripts/activate**
* Once this is activated (you should see (venv) in front of your command line), install the python dependencies
* If not already installed, make sure you have npcap and C++ build tools installed:
 - https://npcap.com/#download ( check windows API compatible mode )
 - https://visualstudio.microsoft.com/visual-cpp-build-tools/
* **pip install -r requirements.txt** from the root directory should install all required pip libraries
* IF PPYSOEM INSTALLATION FAILS: Run this command: pip install git+https://github.com/bnjmnp/pysoem.git

## Usage

#### Setting up the Config_sheet
* Use Excel to edit the configuration sheet "Config_sheet.xlsx" located in the UserInterface Folder.
* On the SPN Tab, the columns we need to edit are "SPN","Channel", "Board_Num", and "type"
* Spn is the index of the slot board out of the entire network. Example, if we have 2 slot boards with all 64 slot boards, SPN would be a value from 1 to 64.
* Channel is the slot that the specific I/O point is plugged into.
* Board_Num is the board index that the I/O point is on. If you have two NGIO boards daisy chained together, you might have two slots both in Slot 8. This index differentiates which board it is on.
* type is simply the slot_type you expect that slot to behave as. Below Are the 6 eligible values for this column:
 - DigitalOutput
 - DigitalInput
 - AnalogInput
 - AnalogOutput
 - PWMInput
 - FrequencyOutput
 
* Entering any of those 6 strings in the type column will set that slot type accordingly on startup
* Save the excel when editing is finished.

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

#### Using the UI
* Each Slot type has its own window, with its slot and board number listed on the left side.
* You should see 7 tabs on a window when main.py starts:
 - DigitalIn
 - DigitalOut
 - AnalogIn 
 - AnalogOut 
 - PWMIn
 - FreqOut
 - Settings
 
##### DigitalIn
* Enter the threshold (in a2d count) and the far-right button will update green or red depending on if the input is above or below the threshold.

##### DigitalOut
* Simply toggle the button to set digital output either high(green) or low(red)

##### AnalogIn
* Click the update button to report the current analog reading (voltage)

##### AnalogOut
*Enter the output a2d count in the text box and click update to set the output

##### PWMIn
* set the analog threshold in a2dcounts in the threshold box, and click update
* The Input Frequency(Hz) and duty cycle(%) will be reported in their respective boxes.

##### FreqOut
* Set the Freq(%) and duty cycle(%) in both boxes and click update to set the output.

##### Settings
* You can manually update a slot's type with set slot status
* Enter the board and slot number, as well as the desired type (1-6) and click update to see the slot LED change
* Reconnect to EtherCAT by simply clicking connect.
* This is useful if you have to power cycle the boards without having to restart the UI.
