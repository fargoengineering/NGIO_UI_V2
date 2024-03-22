import pysoem
import struct
import collections
import time

class etherCAT:
    
    PRODUCT_CODE = 0xBEEF       # FEI NGIO BOARD ID
    VENDOR_ID = 0x00000EEA      # Fargo Engineering Inc.
    
    slot_type = 0
    
    def __init__(self,ob1):  
        """
        Initializes an instance of the 'etherCAT' class.

        Parameters:
        - ob1 (object): An object representing the global variables for the EtherCAT communication.

        Attributes:
        - master: An instance of pysoem.Master for EtherCAT communication.
        - ec_adapter_name (str): The name of the Ethernet adapter, formatted according to the platform (Linux/Windows).
        - _expected_slave_mapping (dict): Dictionary defining expected EtherCAT slaves and their configurations.
        - slot_command (list): List to store 192-byte PDO arrays for slot command bytes.
        - slot_data (list): List to store 192-byte PDO arrays for slot data (64 bytes each).
        - slot_aux (list): List to store 192-byte PDO arrays for auxiliary data (slot type, BLE status, etc.).
        - slot_command_in (list): List to store 192-byte PDO arrays for incoming slot command bytes.
        - slot_data_in (list): List to store 192-byte PDO arrays for incoming slot data.
        - slot_aux_in (list): List to store 192-byte PDO arrays for incoming auxiliary data.
        - pack_format (str): Format string for struct packing of PDO arrays.
        - gd: Object representing global variables for UI app.

        Note:
        - The 'ec_adapter_name' attribute should be set with the appropriate Ethernet adapter name based on the platform.
        - The '_expected_slave_mapping' dictionary defines the expected EtherCAT slaves with their names, product codes, and configuration functions.
        """
        self.master = pysoem.Master()
        # self.ec_adapter_name = "eth0"      # linux format 
        self.ec_adapter_name = "\\Device\\NPF_{EA8715FA-3EDA-44ED-ACDD-CD45A7D2C462}"   # Windows Format
        SlaveSet = collections.namedtuple('SlaveSet', 'slave_name product_code config_func')
        self._expected_slave_mapping = {0: SlaveSet('FEI_SLAVE', self.PRODUCT_CODE, None)}        
        
        # 192 byte PDO arrays
        self.slot_command = [0] * 32          # slot command byte
        self.slot_data = [0] * 32             # slot data [64 bytes]
        self.slot_aux = [0] * 32              # slot auxillary data (i.e slot type, ble status)
        self.slot_command_in = [0] * 32
        self.slot_data_in = [0] * 32
        self.slot_aux_in = [0] * 32
        self.pack_format  = '@32l32B32B'
        self.gd = ob1
                
    def set_types(self):
        """
        Sets the initial types for EtherCAT communication.

        This method iterates through the Signal Pin Numbers (SPNs) in the global variable 'spn_list' and configures the
        EtherCAT PDO arrays based on the signal types specified in the 'type_dict' attribute of the global variables.

        Types and corresponding PDO configurations:
        - 'digin': Digital Input
        - 'digout': Digital Output
        - 'voltin': Voltage Input
        - 'voltout': Voltage Output
        - 'pwmin': Pulse Width Modulation Input
        - 'freqout': Frequency Output

        Note:
        - The 'update_pdo' method is called with specific parameters for each signal type.
        - A delay of 0.01 seconds is introduced between PDO updates using 'time.sleep(0.01)'.
        """
        for spn in self.gd.spn_list:
            board_num = self.gd.board_dict[spn]
            slot = self.gd.channel_dict[spn]
            self.slot_command[slot-1] = 5
            if self.gd.type_dict[spn] == 'digin':
                self.update_pdo(5,slot,board_num,1,1,1,slot,2)
                time.sleep(.01)
                self.update_pdo(9,slot,board_num,1,1,1,1,slot)
            elif self.gd.type_dict[spn] == 'digout':
                self.update_pdo(5,slot,board_num,1,1,1,slot,1)
                time.sleep(.01)
                self.update_pdo(9,slot,board_num,1,1,1,1,slot)
            elif self.gd.type_dict[spn] == 'voltin':
                self.update_pdo(5,slot,board_num,1,1,1,slot,3)
                time.sleep(.01)
                self.update_pdo(9,slot,board_num,1,1,1,1,slot)
            elif self.gd.type_dict[spn] == 'voltout':
                self.update_pdo(5,slot,board_num,1,1,1,slot,4)
                time.sleep(.01)
                self.update_pdo(9,slot,board_num,1,1,1,1,slot)
            elif self.gd.type_dict[spn] == 'pwmin':
                self.update_pdo(5,slot,board_num,1,1,1,slot,5)
                time.sleep(.01)
                self.update_pdo(9,slot,board_num,1,1,1,1,slot)
            elif self.gd.type_dict[spn] == 'freqout':
                self.update_pdo(5,slot,board_num,1,1,1,slot,6)
                time.sleep(.01)
                self.update_pdo(9,slot,board_num,1,1,1,1,slot)
                         
            
    def pack_output(self):
        """
        Packs the slot values into a binary output for EtherCAT communication.

        This method converts the slot values for command, data, and auxiliary data into integer lists.
        The integer lists are then packed using the struct.pack method, following the specified 'pack_format'.

        Returns:
        - packed_output (bytes): A binary-packed representation of the 192-byte PDO arrays.

        Note:
        - The 'pack_format' attribute defines the packing format for struct.pack.
        - The resulting packed_output can be sent over EtherCAT for communication.
        """
        # Convert all slot values to integers
        command_values = [int(val) for val in self.slot_command[:32]]
        data_values = [int(val) for val in self.slot_data[:32]]
        aux_values = [int(val) for val in self.slot_aux[:32]]
        self.packed_output = struct.pack(self.pack_format, *data_values, *command_values, *aux_values)   #192        
        return self.packed_output
    
    def unpack_input(self,packed_input):
        """
        Unpacks the received binary input from EtherCAT into separate arrays.

        Parameters:
        - packed_input (bytes): The binary-packed input received from EtherCAT.

        Returns:
        - unpacked_values (tuple): A tuple containing three arrays representing unpacked command, data, and auxiliary data.

        Note:
        - The 'pack_format' attribute is used to determine the unpacking format.
        - The unpacked values are stored in 'self.slot_command_in', 'self.slot_data_in', and 'self.slot_aux_in'.
        """
        # Unpack the packed data into three separate arrays
        unpacked_values = struct.unpack(self.pack_format, packed_input)
        # Update self.slot_command with the first 32 values
        self.slot_command_in = list(unpacked_values[32:64])
        # Update self.slot_data with the next 32*4 value
        self.slot_data_in = list(unpacked_values[:32]) # 32:64
        # Update self.slot_aux with the last 32 values
        self.slot_aux_in = list(unpacked_values[64:]) # 64:
        return unpacked_values
        
    def run_ec(self):        
        """
        Configures and starts the EtherCAT communication.

        This method performs the following steps:
        1. Closes the EtherCAT communication if there are existing slaves.
        2. Opens the EtherCAT master with the specified adapter name.
        3. Initializes the master configuration and prints information about connected slaves.
        4. Configures the slave mapping.
        5. Waits for 50 ms for slaves to reach the SAFEOP_STATE.
        6. Checks if all slaves have reached the OP_STATE, raising an exception if not.
        7. Sets the master state to OP_STATE and writes the state.
        8. Checks if all slaves have reached the OP_STATE after transitioning.

        Note:
        - The 'ec_adapter_name' attribute should be set with the appropriate Ethernet adapter name based on the platform.
        - The 'pysoem' module is assumed to be imported and used for EtherCAT communication.
        """

            
        self.master.open(self.ec_adapter_name)   # make sure matching correct platform
        
        if self.master.config_init() > 0:            
            for i,slave in enumerate(self.master.slaves):
                print(f"Slave {i} name: {slave.name}")
                
            self.master.config_map()
            
            # wait 50 ms for slaves to reach SAFE_OP state
            if self.master.state_check(pysoem.SAFEOP_STATE, 50000) != pysoem.SAFEOP_STATE:
                self.master.read_state()
                for slave in self.master.slaves:
                    if not slave.state == pysoem.OP_STATE:
                        print(f"{slave.name} did not reach OP state")
                # raise Exception('not all slaves reached OP state')
            
            # go to OP state    
            self.master.state = pysoem.OP_STATE
            self.master.write_state()

            self.master.state_check(pysoem.OP_STATE, 50000)
            if self.master.state != pysoem.OP_STATE:
                self.master.read_state()
                for slave in self.master.slaves:
                    if not slave.state == pysoem.OP_STATE:
                        print('{} did not reach OP state'.format(slave.name))
                raise Exception('not all slaves reached OP state')
                
    def update_pdo(self,command,slot_number,board_number,data1,data2,data3,data4,data5):     
        """
        Updates the PDO arrays with specified values and sends the output to EtherCAT.

        Parameters:
        - command (int): The command value for the PDO.
        - slot_number (int): The slot number for updating the PDO arrays.
        - board_number (int): The board number corresponding to the EtherCAT slave.
        - data1 to data4 (int): Values to be packed into the PDO data array.
        - data5 (int): Value to be updated in the PDO auxiliary array.

        Note:
        - The 'pack_output' method is used to pack the updated PDO arrays.
        - If the specified board_number is not found, a message is printed.
        - The EtherCAT process data is sent and received, and a delay of 0.05 seconds is introduced.
        """
        # SEND OUTPUT PDO
        # 192 byte code: 
        self.slot_command[int(slot_number)-1] = command        
        # MSB
        values = [int(byte) for byte in [data1, data2, data3, data4]]
        shifted_vals = [value << (8 * (3 - i)) for i, value in enumerate(values)]
        data_out = sum(shifted_vals)

        self.slot_data[int(slot_number)-1] = data_out
        self.slot_aux[int(slot_number)-1] = data5
        try:
            self.master.slaves[board_number-1].output = self.pack_output()
        except:
            # print(f"Board #{board_number} not found!")
            pass
        self.master.send_processdata()   
        self.master.receive_processdata(5000)     
        time.sleep(0.05) 
        
    def read_pdo_voltage(self,slot_num):
        """
        Reads the voltage value from the specified slot in the Input PDO.

        Parameters:
        - slot_num (int): The slot number to read from in the Input PDO.

        Returns:
        - voltage (float): The converted voltage value.

        Note:
        - The 'send_processdata' and 'receive_processdata' methods are used to update the Input PDO.
        - The 'unpack_input' method is used to unpack the received binary input from EtherCAT.
        - The 'split_bytes' and 'adc_to_voltage' methods are assumed to be implemented for further processing.
        - If the EtherCAT device is not online, an IndexError is caught and an appropriate message is printed.
        """
        # Read Input PDO
        self.master.send_processdata()
        self.master.receive_processdata(2000)
        try:
            voltage__bytes = self.master.slaves[0].input
            self.unpack_input(voltage__bytes)
            print(str(self.slot_data_in))
            data = self.slot_data_in[slot_num-1]
            vals = self.split_bytes(data)
            voltage = self.adc_to_voltage(vals[0])
            return(voltage)
            # return(vals[0]) # raw A2D
        except IndexError as e:
            print(e)
            print("EtherCAT Device Not Online!")
            
    def read_pdo_pwm(self,slot_num):
        """
        Reads the PWM duty cycle and frequency from the specified slot in the Input PDO.

        Parameters:
        - slot_num (int): The slot number to read from in the Input PDO.

        Returns:
        - duty (int): The PWM duty cycle value.
        - freq (int): The PWM frequency value.

        Note:
        - The 'send_processdata' and 'receive_processdata' methods are used to update the Input PDO.
        - The 'unpack_input' method is used to unpack the received binary input from EtherCAT.
        - The 'split_bytes' method is assumed to be implemented for further processing.
        - If the EtherCAT device is not online, an IndexError is caught, and an appropriate message is printed.
        - Any frequency spikes are rounded to anticipated values (1000, 500, or 100).
        """
         # Read Input PDO, return only data 3 (digital in or pwm in value)
        self.master.send_processdata()
        self.master.receive_processdata(2000)
        try:
            bytes = self.master.slaves[0].input
            self.unpack_input(bytes)
            data = self.slot_data_in[slot_num-1]
            vals = self.split_bytes(data)
            duty = vals[0]
            freq = vals[1]           
            
            # Round any frequency spikes to the anticipated values
            if 935 < freq < 1050:
                freq = 1000
            elif 450 < freq <550:
                freq = 500
            elif 50 < freq < 150:
                freq = 100
                
            return duty,freq
        except IndexError as e:
            print(e)
            print("EtherCAT Device Not Online!")
        
    def close_ec(self):
        """
        Closes the EtherCAT communication.

        This method sets the master state to INIT_STATE, requests INIT state for all slaves, and closes the EtherCAT master.

        Note:
        - A delay of 1 second is introduced after setting the INIT_STATE and writing the state.
        - Another delay of 1 second is introduced before closing the EtherCAT master.
        """
        self.master.state = pysoem.INIT_STATE
        # request INIT state for all slaves
        self.master.write_state()
        time.sleep(1)
        self.master.close()
        time.sleep(1)

    def adc_to_voltage(self,adc_value):
        # Define the ADC range and corresponding voltage range
        adc_min = 0
        adc_max = 4096
        voltage_min = 0.0
        voltage_max = 17.5

        # Calculate the voltage using linear interpolation
        voltage = voltage_min + (adc_value - adc_min) * (voltage_max - voltage_min) / (adc_max - adc_min)
        # Ensure voltage is not below zero
        voltage = max(voltage, 0.0)
        # Round to two decimal places
        voltage = round(voltage, 2)

        return voltage

    def pack_bytes_to_pdo(self,byteArray):
        """
        Converts ADC (Analog-to-Digital Converter) value to voltage.

        Parameters:
        - adc_value (int): The ADC value to be converted.

        Returns:
        - voltage (float): The calculated voltage.

        Note:
        - Assumes an ADC range from 0 to 4096 and a corresponding voltage range from 0.0 to 17.5.
        - Uses linear interpolation to calculate the voltage.
        - Ensures the voltage is not below zero.
        - Rounds the calculated voltage to two decimal places.
        """
        if len(byteArray) != 8:
            raise ValueError("Input byteArray must contain exactly 8 values")

        # Use the 'Q' format specifier to pack into an unsigned long long (64 bits)
        packed_value = struct.pack('Q', *byteArray)
        # Unpack the bytes to a 64-bit integer (unsigned long long)
        unpacked_value = struct.unpack('Q', packed_value)[0]

        return unpacked_value

    def set_slot(self):    
        """
        Sets the EtherCAT slot based on user input.

        This method retrieves slot number, board number, and type from user input fields and
        calls the 'update_pdo' method to update the PDO arrays with the specified values.

        Note:
        - Assumes the existence of user input fields 'gd.slot_num_box', 'gd.board_box', and 'gd.aux_box'.
        - The 'update_pdo' method is called with command=5, and the specified slot, board, and type values.
        """
        slot_num = int(self.gd.slot_num_box.get())
        board_num = int(self.gd.board_box.get())
        type = int(self.gd.aux_box.get())
        self.update_pdo(5,slot_num,board_num,1,1,1,1,type)
        
    def split_bytes(self,long):
        """
        Splits a long integer into two 16-bit values.

        Parameters:
        - long_value (int): The long integer to be split.

        Returns:
        - data1 (int): The first 16 bits of the long integer.
        - data2 (int): The last 16 bits of the long integer.
        """
        data1 = (long >> 16) & 0xFFFF
        data2 = long & 0xFFFF
        return data1, data2