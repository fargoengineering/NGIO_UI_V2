from global_defines import *
import time
from ethercat import *
key_battery_init_count = 0


class ui_callbacks:

    global _uc, _dv, io_ob, can2

    def __init__(self, ob1,ec):
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