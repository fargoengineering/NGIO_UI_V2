from global_defines import *
import time
from ethercat import *
key_battery_init_count = 0


class ui_callbacks:

    global _uc, _ec

    def __init__(self,ob1,ec):
        """
        Initializes an instance of the 'ui_callbacks' class.

        Parameters:
        - ob1: An object representing the global variables for UI callbacks.
        - ec: An object representing the 'etherCAT' class for EtherCAT communication.
        """
        self._uc = ob1  # add dictionary to glcc
        self._ec = ec
        
    def dig_in_uc(self, i):
        """
        Handles digital input functionality for the UI.

        Parameters:
        - i (int): Index corresponding to the digital input in UI elements.

        Note:
        - Reads the digital input Signal Pin Number (SPN) and retrieves associated board and slot numbers.
        - Retrieves the threshold value from the corresponding UI entry field.
        - Prints the threshold and input values for debugging purposes.
        - Calls the 'read_pdo_voltage' method from the 'etherCAT' class to read the voltage from the specified slot.
        - Compares the input voltage with the threshold and updates the UI button color accordingly.
        """
        sp = self._uc.dig_ip_spn[i]
        board_num = int(self._uc.board_dict[sp])
        slot_num = int(self._uc.channel_dict[sp])        
        # Probably need to store in a global variable
        if (self._uc.dig_ip_entry[i].get() == ''):
            threshold = 0
        else:
            threshold = float(self._uc.dig_ip_entry[i].get())   
        print("threshold: "+str(threshold))   
        input = self._ec.read_pdo_voltage(slot_num)
        print("input: "+str(input))
        # This part should be in the update_ui thread
        if(input > threshold):
            self._uc.dig_ip_button[i].config(background = "green")
        else:
            self._uc.dig_ip_button[i].config(background = "red")
        print("DigIN "+str(sp))

    def dig_out_uc(self, i):        
        """
        Handles digital output functionality for the UI.

        Parameters:
        - i (int): Index corresponding to the digital output in UI elements.

        Note:
        - Reads the digital output Signal Pin Number (SPN) and retrieves associated board and slot numbers.
        - Checks the background color of the UI button to determine the current state (LOW or HIGH).
        - Calls the 'update_pdo' method from the 'etherCAT' class to update the PDO arrays based on the button state.
        - Updates the UI button color accordingly.
        """        
        sp = self._uc.dig_op_spn[i]
        board_num = int(self._uc.board_dict[sp])
        slot_num = int(self._uc.channel_dict[sp])
    
        if(self._uc.dig_op_button[i].cget("background")=="green"):
            # Set to LOW
            self._ec.update_pdo(5,slot_num,board_num,0,0,0,slot_num,1)
            self._ec.update_pdo(9,slot_num,board_num,0,0,0,0,slot_num)
            self._uc.dig_op_button[i].config(background = "red")
        else:
            self._ec.update_pdo(5,slot_num,board_num,1,1,0,slot_num,1)
            self._ec.update_pdo(9,slot_num,board_num,0,0,0,0,slot_num)
            self._uc.dig_op_button[i].config(background = "green")
        print("DIGOUT "+str(sp))
        
    def volt_in_uc(self, i):
        """
        Handles voltage input functionality for the UI.

        Parameters:
        - i (int): Index corresponding to the voltage input in UI elements.

        Note:
        - Reads the voltage input Signal Pin Number (SPN) and retrieves associated board and slot numbers.
        - Ensures that the board is set to analog input by calling 'update_pdo' method from the 'etherCAT' class.
        - Calls the 'read_pdo_voltage' method from the 'etherCAT' class to read the voltage from the specified slot.
        - Updates the text box in the UI with the input voltage value.
        """
        sp = self._uc.vol_ip_spn[i]
        board_num = int(self._uc.board_dict[sp])
        slot_num = int(self._uc.channel_dict[sp])
        
        # Make sure the board is analog in
        self._ec.update_pdo(5,slot_num,board_num,0,0,0,0,3)
        self._ec.update_pdo(9,slot_num,board_num,0,0,0,0,slot_num)
        volt_in = self._ec.read_pdo_voltage(slot_num)
        
        # Update the text box with input voltage
        self._uc.volt_ip_label[i].delete(0,END)
        self._uc.volt_ip_label[i].insert(0,str(volt_in))
        
        print("VoltIN "+str(sp))

    def volt_out_uc(self, i):
        """
        Handles voltage output functionality for UI callbacks.

        Parameters:
        - i (int): Index corresponding to the voltage output in UI elements.

        Note:
        - Reads the voltage output Signal Pin Number (SPN) and retrieves associated board and slot numbers.
        - Retrieves the voltage output value from the corresponding UI label.
        - Splits the voltage output value into two 8-bit data values.
        - Ensures that the board is set to analog output by calling 'update_pdo' method from the 'etherCAT' class.
        """
        sp = self._uc.vol_op_spn[i]
        board_num = int(self._uc.board_dict[sp])
        slot_num = int(self._uc.channel_dict[sp])
        
        volt_out = int(self._uc.volt_op_label[i].get())
        
        data1 = (volt_out >> 8) & 0xFF
        data2 = volt_out & 0xFF
        
        # Make sure board is analog out
        self._ec.update_pdo(5,slot_num,board_num,data1,data2,0,1,4)     # data 4 =1 to enable tracking output
        self._ec.update_pdo(9,slot_num,board_num,data1,data2,0,0,slot_num)
        
        print("VoltOUT "+str(sp))
        
    def pwm_in_uc(self, i):
        """
        Handles PWM input functionality for the UI.

        Parameters:
        - i (int): Index corresponding to the PWM input in UI elements.

        Note:
        - Reads the PWM input Signal Pin Number (SPN) and retrieves associated board and slot numbers.
        - Retrieves the PWM threshold value from the corresponding UI label and splits it into two 8-bit data values.
        - Ensures that the board is set to PWM input by calling 'update_pdo' method from the 'etherCAT' class.
        - Calls the 'read_pdo_pwm' method from the 'etherCAT' class to read duty cycle and frequency.
        - Updates the UI labels with the read duty cycle and frequency values.
        """
        sp = self._uc.pwm_ip_spn[i]
        board_num = int(self._uc.board_dict[sp])
        slot_num = int(self._uc.channel_dict[sp])
        
        threshold = int(self._uc.pwm_thresh_label[i].get())
        data1 = (threshold >> 8) & 0xFF
        data2 = (threshold & 0xFF)
        
        self._ec.update_pdo(5,slot_num,board_num,data1,data2,0,0,5)
        self._ec.update_pdo(9,slot_num,board_num,data1,data2,0,0,slot_num)
        time.sleep(0.5)
        duty,freq = self._ec.read_pdo_pwm(slot_num)
        
        self._uc.pwm_ip_label_freq[i].delete(0,END)
        self._uc.pwm_ip_label_freq[i].insert(0,freq)
        self._uc.pwm_ip_label_duty[i].delete(0,END)
        self._uc.pwm_ip_label_duty[i].insert(0,duty)
        
        # update the boxes:
        print(duty)
        print(freq)
        print("PWMIN "+str(sp))
        
    def freq_out_uc(self, i):
        """
        Handles frequency output functionality for UI callbacks.

        Parameters:
        - i (int): Index corresponding to the frequency output in UI elements.

        Note:
        - Reads the frequency output Signal Pin Number (SPN) and retrieves associated board and slot numbers.
        - Retrieves the frequency and duty cycle percentage values from the corresponding UI labels.
        - Converts the duty cycle percentage to a 16-bit duty cycle value.
        - Splits the frequency and duty cycle values into four 8-bit data values.
        - Calls the 'update_pdo' method from the 'etherCAT' class to update the PDO arrays based on the input values.
        """
        sp = self._uc.fq_op_spn[i]
        board_num = int(self._uc.board_dict[sp])
        slot_num = int(self._uc.channel_dict[sp])
        
        freq = int(self._uc.freq_label_freq[i].get())
        duty_per = int(self._uc.freq_label_duty[i].get())
        
        duty = int((4096 - ((duty_per/100) * 4096)))        
        
        data1 = (freq >> 8) & 0xFF
        data2 = freq & 0xFF
        data3 = (duty >> 8) & 0xFF
        data4 = duty & 0xFF
        
        print(freq)
        print(duty)
        
        self._ec.update_pdo(5,slot_num,board_num,0,0,0,slot_num,6)  # Can't send all data with command 5, only set slotnum/type
        self._ec.update_pdo(9,slot_num,board_num,data1,data2,data3,data4,slot_num)
    
        print("FREQOUT "+str(sp))
        
    def pot_uc(self, i):
        """
        Handles potentiometer functionality for UI callbacks.

        Parameters:
        - i (int): Index corresponding to the voltage output in UI elements.
        """
        sp = self._uc.pot_spn[i]
        board_num = int(self._uc.board_dict[sp])
        slot_num = int(self._uc.channel_dict[sp])
        
        pot_out = int(self._uc.pot_label[i].get())
        
        # Shift the pot value
        data1 = (pot_out >> 4) & 0x0F
        data2 = pot_out & 0x0F
        
        # Make sure board is potentiometer
        # SEND DATA 1 and DATA2!
        self._ec.update_pdo(5,slot_num,board_num,data1,data2,pot_out,pot_out,7)
        self._ec.update_pdo(9,slot_num,board_num,data1,data2,pot_out,pot_out,slot_num)
        
        print("Potentiometer "+str(sp))
        
    def set_input_relay(self,board,slot,state):
        """
        Sets the input relay state for a specified board and slot.

        Parameters:
        - board (int): The board number.
        - slot (int): The slot number.
        - state (int): The desired state of the relay (0 or 1).

        Note:
        - Sets the relay command and state in the EtherCAT PDO arrays.
        - Attempts to update the EtherCAT master's output with the modified PDO arrays.
        - Resets the PDO to avoid toggling the relay for shorting after a short delay.
        - Prints a message if the specified board is not detected.
        """
        self._ec.slot_command[slot-1] = 7        # set relay command
        self._ec.slot_aux[slot-1] = state        
        try:
            self._ec.master.slaves[board-1].output = self._ec.pack_output()
            self._ec.master.send_processdata()
            self._ec.master.receive_processdata(5000)
            # Reset PDO so we don't keep toggling the relay for shorting..
            time.sleep(0.5)
            self._ec.slot_command[slot-1] = 9
            self._ec.master.slaves[board-1].output = self._ec.pack_output()
            self._ec.master.send_processdata()
            self._ec.master.receive_processdata(5000)
        except:
            print(f"Board #{board} not detected!")
            
    def set_output_relay(self,relay_board,board,channel,state):
        """
        Sets the output relay state for a specified board, channel, and relay board.

        Parameters:
        - relay_board (int): The relay board number.
        - board (int): The board number.
        - channel (int): The channel number.
        - state (int): The desired state of the relay (0 or 1).

        Note:
        - Sets the CAN command, relay board number, and state in the EtherCAT PDO arrays.
        - Attempts to update the EtherCAT master's output with the modified PDO arrays.
        - Resets the PDO to avoid toggling the relay for shorting after a short delay.
        - Prints a message if the specified board is not detected.
        """
        self._ec.slot_command[channel-1] = 13   # send CAN command
        self._ec.slot_data[channel-1] = relay_board               # RELAY BOARD NUMBER, NOT NGIO BOARD NUMBER
        self._ec.slot_aux[channel-1] = state        
        try:
            self._ec.master.slaves[board-1].output = self._ec.pack_output()
            self._ec.master.send_processdata()
            self._ec.master.receive_processdata(5000)
            time.sleep(0.5)
            self._ec.slot_command[channel-1] = 9
            self._ec.master.slaves[board-1].output = self._ec.pack_output()
            self._ec.master.send_processdata()
            self._ec.master.receive_processdata(5000)
        except:
            print(f"Board #{board} not detected!")
            
            
    def relay_send(self,spn,selected_val):                
        """
        Sends relay commands based on the selected value for a specified SPN.

        Parameters:
        - spn (str): The Signal Pin Number (SPN).
        - selected_val (str): The selected value indicating the relay state.

        Note:
        - Retrieves board and slot numbers, relay type, and other relevant information from UI dictionaries.
        - Maps the selected value to the corresponding relay state.
        - Calls either 'set_input_relay' or 'set_output_relay' based on the relay type and sends the command.
        - Adds a delay to ensure the relay commands are processed.
        - Pauses UI for 6 seconds to allow relay function to complete.
        """
        board_num = int(self._uc.board_dict[spn])                   # Board_Num : Column F
        slot_num = int(self._uc.channel_dict[spn])                  # Channel   : Column E
        relay_type = str(self._uc.relay_type_dict[spn])             # IO_type   : Column J
        
        if relay_type == "IN":
            io_type = 1
            if selected_val == "OpenCircuit":
                state = 1
            elif selected_val == "BatteryShort":
                state = 2
            elif selected_val == "GroundShort":
                state = 3
            elif selected_val == "Bypass":
                state = 4          
        elif relay_type == "OUT":
            io_type = 0 
            relay_board = int(self._uc.relay_board_dict[spn])       # CANChannel : Column I
            relay_channel = int(self._uc.relay_channel_dict[spn])   # CANBoardNum : Column H
            if selected_val == "OpenCircuit":
                state = 1
            elif selected_val == "BatteryShort":
                state = 3
            elif selected_val == "GroundShort":
                state = 2
            elif selected_val == "Bypass":
                state = 0          
                        
        if (io_type == 1):
            self.set_input_relay(board_num,slot_num,state)
        elif (io_type == 0):
            self.set_output_relay(relay_board,board_num,relay_channel,state)        
        
        # time.sleep(6)