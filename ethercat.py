import pysoem
import struct
import collections
import time
# from global_defines import *

class etherCAT:
    
    PRODUCT_CODE = 0xBEEF
    VENDOR_ID = 0x00000EEA
    
    slot_type = 0
    
    def __init__(self,ob1):  
        self.master = pysoem.Master()
        # self.gv = global_vars()
        # self.ec_adapter_name = "eth0"      # linux format 
        self.ec_adapter_name = "\\Device\\NPF_{2AFC35B5-1EE7-49B9-927D-D2CE5EDC52DD}"    # Windows Format (-_-)
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
        
    def pause_pdo(self):
        self.slot_command = [0] * 32
        self.slot_data = [0] * 32
        self.slot_aux = [0] * 32
        for slave in self.master.slaves:
            slave.output = self.pack_output()
        self.master.send_processdata()
        self.master.receive_processdata(5000)
        
    def set_types(self):
        print("initial types set")
        c = 5
        for spn in self.gd.spn_list:
            board_num = self.gd.board_dict[spn]
            slot = self.gd.channel_dict[spn]
            self.slot_command[slot-1] = 5
            if self.gd.type_dict[spn] == 'digin':
                self.update_pdo(5,slot,board_num,1,1,1,1,2)
                # self.slot_aux[slot-1] = 2
            elif self.gd.type_dict[spn] == 'digout':
                self.update_pdo(5,slot,board_num,1,1,1,1,1)
                # self.slot_aux[slot-1] = 1
            elif self.gd.type_dict[spn] == 'voltin':
                self.update_pdo(5,slot,board_num,1,1,1,1,3)
                # self.slot_aux[slot-1] = 3
            elif self.gd.type_dict[spn] == 'voltout':
                self.update_pdo(5,slot,board_num,1,1,1,1,4)
                # self.slot_aux[slot-1] = 4
            elif self.gd.type_dict[spn] == 'pwmin':
                self.update_pdo(5,slot,board_num,1,1,1,1,5)
                # self.slot_aux[slot-1] = 5
            elif self.gd.type_dict[spn] == 'freqout':
                self.update_pdo(5,slot,board_num,1,1,1,1,6)
                # self.slot_aux[slot-1] = 6
                         
            
    def pack_output(self):
        # Convert all slot values to integers
        command_values = [int(val) for val in self.slot_command[:32]]
        data_values = [int(val) for val in self.slot_data[:32]]
        aux_values = [int(val) for val in self.slot_aux[:32]]
        self.packed_output = struct.pack(self.pack_format, *data_values, *command_values, *aux_values)   #192        
        return self.packed_output
    
    def unpack_input(self,packed_input):
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
        
        if len(self.master.slaves) > 0:
            self.close_ec()
            
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
        # SEND OUTPUT PDO
        # 192 byte code: 
        self.slot_command[int(slot_number)-1] = command
        # LSB
        # values = [int(byte) for byte in [data1,data2,data3,data4]]
        # shifted_vals = [value << (8 * i) for i, value in enumerate(values)]
        # data_out = sum(shifted_vals)
        
        # MSB
        values = [int(byte) for byte in [data1, data2, data3, data4]]
        shifted_vals = [value << (8 * (3 - i)) for i, value in enumerate(values)]
        data_out = sum(shifted_vals)

        self.slot_data[int(slot_number)-1] = data_out
        self.slot_aux[int(slot_number)-1] = data5
        try:
            self.master.slaves[board_number-1].output = self.pack_output()
        except:
            print(f"Board #{board_number} not found!")
        self.master.send_processdata()   
        self.master.receive_processdata(5000)     
        time.sleep(0.05) 
        
    def read_pdo_voltage(self,slot_num):
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
        voltage_max = 17.25

        # Calculate the voltage using linear interpolation
        voltage = voltage_min + (adc_value - adc_min) * (voltage_max - voltage_min) / (adc_max - adc_min)
        # Ensure voltage is not below zero
        voltage = max(voltage, 0.0)
        # Round to two decimal places
        voltage = round(voltage, 2)

        return voltage

    def pack_bytes_to_pdo(self,byteArray):
        if len(byteArray) != 8:
            raise ValueError("Input byteArray must contain exactly 8 values")

        # Use the 'Q' format specifier to pack into an unsigned long long (64 bits)
        packed_value = struct.pack('Q', *byteArray)
        # Unpack the bytes to a 64-bit integer (unsigned long long)
        unpacked_value = struct.unpack('Q', packed_value)[0]

        return unpacked_value

    def set_slot(self):
        slot_num = int(self.gd.slot_num_box.get())
        board_num = int(self.gd.board_box.get())
        type = int(self.gd.aux_box.get())
        self.update_pdo(5,slot_num,board_num,1,1,1,1,type)
        
    def split_bytes(self,long):
        data1 = (long >> 16) & 0xFFFF
        data2 = long & 0xFFFF
        return data1, data2