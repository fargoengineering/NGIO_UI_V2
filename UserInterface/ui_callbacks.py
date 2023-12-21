from global_defines import *
import time
from ethercat import *
key_battery_init_count = 0


class ui_callbacks:

    global _uc, _ec

    def __init__(self,ob1,ec):
        self._uc = ob1  # add dictionary to glcc
        self._ec = ec
        
    def dig_in_uc(self, i):
        sp = self._uc.dig_ip_spn[i]
        board_num = int(self._uc.board_dict[sp])
        slot_num = int(self._uc.channel_dict[sp])        
        # Probably need to store in a global variable
        if (self._uc.dig_ip_entry[i].get() == ''):
            threshold = 0
        else:
            threshold = float(self._uc.dig_ip_entry[i].get())   
        print("threshold: "+str(threshold))   
        input = self._ec.read_pdo_voltage()      
        print("input: "+str(input))
        # This part should be in the update_ui thread
        if(input > threshold):
            self._uc.dig_ip_button[i].config(background = "green")
        else:
            self._uc.dig_ip_button[i].config(background = "red")
        print("DigIN "+str(sp))

    def dig_out_uc(self, i):        
        sp = self._uc.dig_op_spn[i]
        board_num = int(self._uc.board_dict[sp])
        slot_num = int(self._uc.channel_dict[sp])
    
        if(self._uc.dig_op_button[i].cget("background")=="green"):
            # Set to LOW
            self._ec.update_pdo(5,slot_num,board_num,0,0,0,0,1)
            self._uc.dig_op_button[i].config(background = "red")
        else:
            self._ec.update_pdo(5,slot_num,board_num,1,1,0,0,1)
            self._uc.dig_op_button[i].config(background = "green")
        print("DIGOUT "+str(sp))
        
    def volt_in_uc(self, i):
        sp = self._uc.vol_ip_spn[i]
        board_num = int(self._uc.board_dict[sp])
        slot_num = int(self._uc.channel_dict[sp])
        
        # Make sure the board is analog in
        self._ec.update_pdo(5,slot_num,board_num,0,0,0,0,3)
        volt_in = self._ec.read_pdo_voltage()
        
        # Update the text box with input voltage
        self._uc.volt_ip_label[i].delete(0,END)
        self._uc.volt_ip_label[i].insert(0,str(volt_in))
        
        print("VoltIN "+str(sp))

    def volt_out_uc(self, i):
        sp = self._uc.vol_op_spn[i]
        board_num = int(self._uc.board_dict[sp])
        slot_num = int(self._uc.channel_dict[sp])
        
        volt_out = int(self._uc.volt_op_label[i].get())
        
        data1 = (volt_out >> 8) & 0xFF
        data2 = volt_out & 0xFF
        
        # Make sure board is analog out
        self._ec.update_pdo(5,slot_num,board_num,data1,data2,0,0,4)
        
        print("VoltOUT "+str(sp))
        
    def pwm_in_uc(self, i):
        sp = self._uc.pwm_ip_spn[i]
        board_num = int(self._uc.board_dict[sp])
        slot_num = int(self._uc.channel_dict[sp])
        
        threshold = int(self._uc.pwm_thresh_label[i].get())
        data1 = (threshold >> 8) & 0xFF
        data2 = (threshold & 0xFF)
        
        self._ec.update_pdo(5,slot_num,board_num,data1,data2,0,0,5)
        time.sleep(0.5)
        duty,freq = self._ec.read_pdo_pwm()
        
        self._uc.pwm_ip_label_freq[i].delete(0,END)
        self._uc.pwm_ip_label_freq[i].insert(0,freq)
        self._uc.pwm_ip_label_duty[i].delete(0,END)
        self._uc.pwm_ip_label_duty[i].insert(0,duty)
        
        # update the boxes:
        print(duty)
        print(freq)
        print("PWMIN "+str(sp))
        
    def freq_out_uc(self, i):
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
        
        self._ec.update_pdo(5,slot_num,board_num,data1,data2,data3,data4,6)
    
        print("FREQOUT "+str(sp))
        
    def set_input_relay(self,board,slot,state):
        self._ec.slot_command[slot-1] = 7        # set relay command
        self._ec.slot_aux[slot-1] = state        
        try:
            self._ec.master.slaves[board-1].output = self._ec.pack_output()
            self._ec.master.send_processdata()
            self._ec.master.receive_processdata(5000)
            # Reset PDO so we don't keep toggling the relay for shorting..
            time.sleep(0.5)
            self._ec.slot_command[slot-1] = 0
            self._ec.master.slaves[board-1].output = self._ec.pack_output()
            self._ec.master.send_processdata()
            self._ec.master.receive_processdata(5000)
        except:
            print(f"Board #{board} not detected!")
            
    def set_output_relay(self,board,channel,state):
        self._ec.slot_command[channel-1] = 13   # send CAN command
        self._ec.slot_data[channel-1] = board               # RELAY BOARD NUMBER, NOT NGIO BOARD NUMBER
        self._ec.slot_aux[channel-1] = state        
        try:
            self._ec.master.slaves[board-1].output = self._ec.pack_output()
            self._ec.master.send_processdata()
            self._ec.master.receive_processdata(5000)
            # Reset PDO?????? ...YES otherwise it will keep doing a short....
            time.sleep(0.5)
            self._ec.slot_command[channel-1] = 0
            self._ec.master.slaves[board-1].output = self._ec.pack_output()
            self._ec.master.send_processdata()
            self._ec.master.receive_processdata(5000)
        except:
            print(f"Board #{board} not detected!")
            
            
    def relay_send(self,spn,selected_val):                
        board_num = int(self._uc.board_dict[spn])                   # Board_Num : Column F
        slot_num = int(self._uc.channel_dict[spn])                  # Channel   : Column E
        relay_type = str(self._uc.relay_type_dict[spn])             # IO_type   : Column J
        
        if relay_type == "IN":
            io_type = 1
        elif relay_type == "OUT":
            io_type = 0 
            relay_board = int(self._uc.relay_board_dict[spn])       # CANChannel : Column I
            relay_channel = int(self._uc.relay_channel_dict[spn])   # CANBoardNum : Column H
            
        if selected_val == "OpenCircuit":
            state = 1
        elif selected_val == "BatteryShort":
            state = 2
        elif selected_val == "GroundShort":
            state = 3
        elif selected_val == "Bypass":
            state = 4          
                        
        if (io_type == 1):
            self.set_input_relay(board_num,slot_num,state)
        elif (io_type == 0):
            self.set_output_relay(relay_board,relay_channel,state)        