from global_defines import *
import time

key_battery_init_count = 0


class ui_callbacks:

    global _uc, _dv, io_ob, can2

    def __init__(self, ob1):
        self._uc = ob1  # add dictionary to glcc
        
    def dig_in_uc(self, i):
        sp = self._uc.dig_ip_spn[i]
        # brd_num = int(self._uc.board_dict[sp])
        # rel_num = int(self._uc.channel_dict[sp])
        # current_data = int(self._uc.UI_dict[sp])
        # new_data = 1 - current_data
        # self._uc.dig_state[sp] = 1 - self._uc.dig_state[sp]
        # state = self._uc.dig_state[sp]
        # self.pass_to_board(spn_number=sp, data=new_data)
        print("DigIN "+str(sp))

    def dig_out_uc(self, i):
        # new_data = self._uc.volt_string[i].get()
        sp = self._uc.dig_op_spn[i]
        # self.pass_to_board(spn_number=sp, data=new_data)
        # self._uc.label_update = 1
        print("DIGOUT "+str(sp))
        
    def volt_in_uc(self, i):
        sp = self._uc.vol_ip_spn[i]
        # brd_num = int(self._uc.board_dict[sp])
        # rel_num = int(self._uc.channel_dict[sp])
        # current_data = int(self._uc.UI_dict[sp])
        # new_data = 1 - current_data
        # self._uc.volt_state[sp] = 1 - self._uc.volt_state[sp]
        # state = self._uc.volt_state[sp]
        # self.pass_to_board(spn_number=sp, data=new_data)
        # self.can2.flip_one(brd_num, rel_num, state)
        print("VoltIN "+str(sp))

    def volt_out_uc(self, i):
        sp = self._uc.vol_op_spn[i]
        # brd_num = int(self._uc.board_dict[sp])
        # rel_num = int(self._uc.channel_dict[sp])
        # current_data = int(self._uc.UI_dict[sp])
        # new_data = 1 - current_data
        # self._uc.freq_state[sp] = 1 - self._uc.freq_state[sp]
        # state = self._uc.freq_state[sp]
        # self.pass_to_board(spn_number=sp, data=new_data)
        # self.can2.flip_one(brd_num, rel_num, state)
        print("VoltOUT "+str(sp))
        
    def pwm_in_uc(self, i):
        sp = self._uc.pwm_ip_spn[i]
        # brd_num = int(self._uc.board_dict[sp])
        # rel_num = int(self._uc.channel_dict[sp])
        # current_data = int(self._uc.UI_dict[sp])
        # new_data = 1 - current_data
        # self._uc.pwm_state[sp] = 1 - self._uc.pwm_state[sp]
        # state = self._uc.pwm_state[sp]
        # self.pass_to_board(spn_number=sp, data=new_data)
        # self.can2.flip_one(brd_num, rel_num, state)
        print("PWMIN "+str(sp))
        
    def freq_out_uc(self, i):
        # new_data = self._uc.freq_string[i].get()
        sp = self._uc.fq_op_spn[i]
        # self.pass_to_board(spn_number=sp, data=new_data)
        # self._uc.label_update = 1
        print("FREQOUT "+str(sp))