import tkinter as tk
from tkinter import ttk
from functools import partial
from UserInterface.update_ui import *
from UserInterface.ui_callbacks import *
from global_defines import *



class generate_ui:
    """
    This module is responsible for initializing each component of the UI, as well as it's grid placement.
    """

    global _ge, ui, ui_call

    def __init__(self, ob1,ec):
        """
        Constructor used to create an instance of generate_ui.

        :param ob1 (Object): Used to pass an instance of global_defines.
        :param ob2 (Object): Used to pass an instance of IOCtrl.
        """
        self._ge = ob1
        self._ge.dig_ip_options = ["Open_Circuit"]
        self.ui_call = ui_callbacks(self._ge,ec)
        self._ec = ec


    # Generates first 7 UI Tabs
    def generate_spn_ui(self):
        """
        The function `generate_spn_ui` is responsible for creating these UI tabs and their widgets:

        DIG I/P | DIG O/P | VOL IN | VOL OUT | PWM IN | FREQ OUT
        """
        # Digital Input Tab
        for i in range(len(self._ge.dig_ip_spn)):
            self._ge.dig_ip_entry.append(0)
            self._ge.dig_ip_update.append(0)
            self._ge.dig_ip_button.append(0)
            self._ge.dig_ip_option.append(0)
            # self._ge.dig_ip_option_var.append(tk.StringVar())
            
            self._ge.dig_ip_entry[i] = tk.Entry(
                self._ge.dig_ip_frame,
                bd=2,
                validate="key",
                width=6,
                font=("courier", 10),
                textvariable=self._ge.dig_ip_str[i],
            )
            
            self._ge.dig_ip_update[i] = tk.Button(
                self._ge.dig_ip_frame,
                height=1,
                width=11,
                bd=8,
                fg="white",
                font=("Geneva", 6),
                text="Update",
                bg="Steel Blue",
                command=partial(self.ui_call.dig_in_uc, i),
            )

            self._ge.dig_ip_button[i] = tk.Button(
                self._ge.dig_ip_frame,
                height=1,
                width=4,
                bd=6,
                state="disabled",
                fg="black",
                font=("Geneva", 6),
                bg="Green",
                command=partial(self.ui_call.dig_in_uc, i),
            )

            self._ge.dig_ip_option[i] = tk.OptionMenu(
                self._ge.dig_ip_frame,
                tk.StringVar(self._ge.dig_ip_frame),
                *self._ge.dropdown_relay_options,
                command=partial(self.ui_call.relay_send, self._ge.dig_ip_spn[i])
            )

            label = tk.Label(
                self._ge.dig_ip_frame,
                text=self._ge.dig_ip_name[i],
                bg="azure3",
                width=30,
            )

            self._ge.dig_ip_mode.update({i: 0})

            spn = self._ge.dig_ip_spn[i]
            
            # bno = self._ge.board_dict[spn]
            # tempList = []
            # if bno in self._ge.board_wid_dict:
            #     tempList = self._ge.board_wid_dict[bno]
            # tempList.append(self._ge.dig_ip_option[i])
            # self._ge.board_wid_dict.update({bno: tempList})

            # first column
            if i < 19:
                label.grid(row=i, column=0)
                self._ge.dig_ip_entry[i].grid(row=i,column=1)
                self._ge.dig_ip_update[i].grid(row=i,column=2)
                self._ge.dig_ip_button[i].grid(row=i,column=3)
                if self._ge.relay_bool_dict.get(self._ge.dig_ip_spn[i]):
                    self._ge.dig_ip_option[i].grid(row=i,column=4)
            # second column
            else:
                label.grid(row=i - 19, column=5)
                self._ge.dig_ip_entry[i].grid(row=i-19,column=6)
                self._ge.dig_ip_update[i].grid(row=i-19,column=7)
                self._ge.dig_ip_button[i].grid(row=i-19, column=8)
                if self._ge.relay_bool_dict.get(self._ge.dig_ip_spn[i]):
                    self._ge.dig_ip_option[i].grid(row=i-19,column=9)

        # Digital Output Tab
        for i in range(len(self._ge.dig_op_spn)):
            self._ge.dig_op_button.append(0)
            self._ge.dig_op_option.append(0)
            self._ge.dig_op_button[i] = tk.Button(
                self._ge.dig_op_frame,
                height=1,
                width=4,
                bd=6,
                fg="black",
                font=("Geneva", 6),
                bg="red",
                command=partial(self.ui_call.dig_out_uc, i),
            )
            label = tk.Label(
                self._ge.dig_op_frame,
                text=self._ge.dig_op_name[i],
                bg="azure3",
                width=30,
            )
            
            self._ge.dig_op_option[i] = tk.OptionMenu(
                self._ge.dig_op_frame,
                tk.StringVar(self._ge.dig_op_frame),
                *self._ge.dropdown_relay_options,
                command=partial(self.ui_call.relay_send, self._ge.dig_op_spn[i])
            )
            if 0 <= i < 31:
                row = i
                column = 1
            elif 31 <= i < 62:
                row = i - 31
                column = 3
            elif 62 <= i < 94:
                row = i - 62
                column = 5
            label.grid(row=row, column=column + 1)
            self._ge.dig_op_button[i].grid(row=row, column=column + 2)
            if self._ge.relay_bool_dict.get(self._ge.dig_op_spn[i]):
                self._ge.dig_op_option[i].grid(row=row,column=column+3)

        # Voltage In
        for i in range(len(self._ge.vol_ip_spn)):  # length = 58
            self._ge.volt_ip_label.append(0)
            self._ge.volt_ip_button.append(0)
            self._ge.volt_ip_toggle.append(0)
            self._ge.volt_ip_option.append(0)
            self._ge.relay_switch.append(1)
            self._ge.volt_ip_string.append(tk.StringVar())
            label = tk.Label(
                self._ge.volt_ip_frame,
                text=self._ge.vol_ip_name[i],
                bg="azure3",
                width=30,
            )
            header = tk.Label(
                self._ge.volt_ip_frame,
                text=" ",
                bg="azure3",
                width=30,
            )
            in_label = tk.Label(
                self._ge.volt_ip_frame,
                text="VoltageIn: ",
                bg="azure3",
                width=15,
            )
            self._ge.volt_ip_label[i] = tk.Entry(
                self._ge.volt_ip_frame,
                bd=2,
                validate="key",
                width=6,
                font=("courier", 10),
                textvariable=self._ge.volt_ip_string[i],
            )
            self._ge.volt_ip_button[i] = tk.Button(
                self._ge.volt_ip_frame,
                height=1,
                width=11,
                bd=8,
                fg="white",
                font=("Geneva", 6),
                text="Update",
                bg="Steel Blue",
                command=partial(self.ui_call.volt_in_uc, i),
            )
            self._ge.volt_ip_toggle[i] = tk.Button(
                self._ge.volt_ip_frame,
                height=1,
                width=4,
                bd=6,
                fg="black",
                font=("Geneva", 6),
                bg="Red",
                command=partial(self.ui_call.volt_in_uc, i),
            )
            self._ge.volt_ip_option[i] = tk.OptionMenu(
                self._ge.volt_ip_frame,
                tk.StringVar(self._ge.volt_ip_frame),
                *self._ge.dropdown_relay_options,
                command=partial(self.ui_call.relay_send, self._ge.vol_ip_spn[i])
            )

            if i < 29:
                header.grid(row=0,column=0)
                label.grid(row=i+1, column=0)
                in_label.grid(row=0,column=1)
                self._ge.volt_ip_label[i].grid(row=i+1, column=1)
                self._ge.volt_ip_button[i].grid(row=i+1, column=2)
                if self._ge.relay_bool_dict.get(self._ge.vol_ip_spn[i]):
                    self._ge.volt_ip_option[i].grid(row=i+1,column=3)
            else:
                label.grid(row=i - 28, column=4)
                self._ge.volt_ip_label[i].grid(row=i - 28, column=5)
                self._ge.volt_ip_button[i].grid(row=i - 28, column=6)
                if self._ge.relay_bool_dict.get(self._ge.dig_op_spn[i]):
                    self._ge.volt_ip_option[i].grid(row=i-28,column=7)

            self._ge.volt_ip_label[i].insert(0, "0")
            
        # Voltage Out
        for i in range(len(self._ge.vol_op_spn)):  # length = 58
            self._ge.volt_op_label.append(0)
            self._ge.volt_op_button.append(0)
            self._ge.volt_op_toggle.append(0)
            self._ge.volt_op_option.append(0)
            self._ge.relay_switch.append(1)
            self._ge.volt_op_string.append(tk.StringVar())
            label = tk.Label(
                self._ge.volt_op_frame,
                text=self._ge.vol_op_name[i],
                bg="azure3",
                width=30,
            )
            header = tk.Label(
                self._ge.volt_op_frame,
                text=" ",
                bg="azure3",
                width=30,
            )
            out_label = tk.Label(
                self._ge.volt_op_frame,
                text="VoltageOut: ",
                bg="azure3",
                width=15,
            )
            self._ge.volt_op_label[i] = tk.Entry(
                self._ge.volt_op_frame,
                bd=2,
                validate="key",
                width=6,
                font=("courier", 10),
                textvariable=self._ge.volt_op_string[i],
            )
            self._ge.volt_op_button[i] = tk.Button(
                self._ge.volt_op_frame,
                height=1,
                width=11,
                bd=8,
                fg="white",
                font=("Geneva", 6),
                text="Update",
                bg="Steel Blue",
                command=partial(self.ui_call.volt_out_uc, i),
            )
            self._ge.volt_op_toggle[i] = tk.Button(
                self._ge.volt_op_frame,
                height=1,
                width=4,
                bd=6,
                fg="black",
                font=("Geneva", 6),
                bg="Red",
                command=partial(self.ui_call.volt_out_uc, i),
            )
            self._ge.volt_op_option[i] = tk.OptionMenu(
                self._ge.volt_op_frame,
                tk.StringVar(self._ge.volt_op_frame),
                *self._ge.dropdown_relay_options,
                command=partial(self.ui_call.relay_send, self._ge.vol_op_spn[i])
            )

            if i < 29:
                header.grid(row=0,column=0)
                label.grid(row=i+1, column=0)
                out_label.grid(row=0,column=1)
                self._ge.volt_op_label[i].grid(row=i+1, column=1)
                self._ge.volt_op_button[i].grid(row=i+1, column=2)
                if self._ge.relay_bool_dict.get(self._ge.vol_op_spn[i]):
                    self._ge.volt_op_option[i].grid(row=i+1,column=3)
            else:
                label.grid(row=i - 28, column=3)
                self._ge.volt_op_label[i].grid(row=i - 28, column=4)
                self._ge.volt_op_button[i].grid(row=i - 28, column=5)
                if self._ge.relay_bool_dict.get(self._ge.volt_op_spn[i]):
                    self._ge.volt_op_option[i].grid(row=i - 28,column=6)

            self._ge.volt_op_label[i].insert(0, "0")
            
        # PWM Input Tab
        for i in range(len(self._ge.pwm_ip_spn)):
            self._ge.pwm_ip_label_freq.append(0)
            self._ge.pwm_ip_label_duty.append(0)
            self._ge.pwm_thresh_label.append(0)
            self._ge.pwm_ip_button.append(0)
            self._ge.pwm_ip_option.append(0)
            self._ge.pwm_ip_toggle.append(0)
            self._ge.pwm_ip_string.append(tk.StringVar())
            label = tk.Label(
                self._ge.pwm_ip_frame,
                text=self._ge.pwm_ip_name[i],
                bg="azure3",
                width=30,
            )
            header = tk.Label(
                self._ge.pwm_ip_frame,
                text="  ",
                bg="azure3",
                width=30,
            )
            freq_name = tk.Label(
                self._ge.pwm_ip_frame,
                text="Freq - Hz:",
                bg="azure3",
                width=15,
            )
            thresh_name = tk.Label(
                self._ge.pwm_ip_frame,
                text="Threshold - V:",
                bg="azure3",
                width=15,
            )
            duty_name = tk.Label(
                self._ge.pwm_ip_frame,
                text="Duty %:",
                width=15,
                bg="azure3",
            )
            self._ge.pwm_thresh_label[i] = tk.Entry(
                self._ge.pwm_ip_frame,
                bd=2,
                validate="key",
                width=6,
                font=("courier",10),
            )
            self._ge.pwm_ip_label_freq[i] = tk.Entry(
                self._ge.pwm_ip_frame,
                bd=2,
                validate="key",
                width=6,
                font=("courier", 10),
            )
            self._ge.pwm_ip_label_duty[i] = tk.Entry(
                self._ge.pwm_ip_frame,
                bd=2,
                validate="key",
                width=6,
                font=("courier", 10),
            )

            # Create a Button widget for update
            self._ge.pwm_ip_button[i] = tk.Button(
                self._ge.pwm_ip_frame,
                height=1,
                width=11,
                bd=8,
                fg="white",
                font=("Geneva", 6),
                text="Update",
                bg="Steel Blue",
                command=partial(self.ui_call.pwm_in_uc, i),
            )
            self._ge.pwm_ip_option[i] = tk.OptionMenu(
                self._ge.pwm_ip_frame,
                tk.StringVar(self._ge.pwm_ip_frame),
                *self._ge.dropdown_relay_options,
                command=partial(self.ui_call.relay_send, self._ge.pwm_ip_spn[i])
            )
            
            header.grid(row=0,column=0)
            label.grid(row=i+1, column=0)
            thresh_name.grid(row=0,column=1)
            self._ge.pwm_thresh_label[i].grid(row=i+1,column=1)
            freq_name.grid(row=0,column=2)
            self._ge.pwm_ip_label_freq[i].grid(row=i+1, column=2)
            duty_name.grid(row=0,column=3)
            self._ge.pwm_ip_label_duty[i].grid(row=i+1, column=3)
            self._ge.pwm_ip_button[i].grid(row=i+1, column=4)
            if self._ge.relay_bool_dict.get(self._ge.pwm_ip_spn[i]):
                self._ge.pwm_ip_option[i].grid(row=i+1,column=5)
            
            self._ge.pwm_thresh_label[i].insert(0,"1000")
            self._ge.pwm_ip_label_duty[i].insert(0, "0")
            self._ge.pwm_ip_label_freq[i].insert(0, "0")

        # Freq Tab
        for i in range(len(self._ge.fq_op_spn)):
            self._ge.freq_label_freq.append(0)
            self._ge.freq_label_duty.append(0)
            self._ge.duty_label.append(0)
            self._ge.freq_button.append(0)
            self._ge.freq_op_option.append(0)
            self._ge.freq_toggle.append(0)
            self._ge.freq_string.append(tk.StringVar())
            label = tk.Label(
                self._ge.freq_op_frame,
                text=self._ge.fq_op_name[i],
                bg="azure3",
                width=30,
            )
            header = tk.Label(
                self._ge.freq_op_frame,
                text=" ",
                bg="azure3",
                width=30,
            )
            freq_name = tk.Label(
                self._ge.freq_op_frame,
                text="Freq - Hz:",
                bg="azure3",
                width=15,
            )
            duty_name = tk.Label(
                self._ge.freq_op_frame,
                text="Duty %:",
                bg="azure3",
                width=15,
            )
            self._ge.freq_label_freq[i] = tk.Entry(
                self._ge.freq_op_frame,
                bd=2,
                validate="key",
                width=6,
                font=("courier", 10),
                # textvariable=self._ge.freq_string[i],
            )
            self._ge.freq_label_duty[i] = tk.Entry(
                self._ge.freq_op_frame,
                bd=2,
                validate="key",
                width=6,
                font=("courier", 10),
                # textvariable=self._ge.freq_string[i],
            )
            self._ge.freq_button[i] = tk.Button(
                self._ge.freq_op_frame,
                height=1,
                width=11,
                bd=8,
                fg="white",
                font=("Geneva", 6),
                text="Update",
                bg="Steel Blue",
                command=partial(self.ui_call.freq_out_uc, i),
            )
            self._ge.freq_op_option[i] = tk.OptionMenu(
                self._ge.freq_op_frame,
                tk.StringVar(self._ge.freq_op_frame),
                *self._ge.dropdown_relay_options,
                command=partial(self.ui_call.relay_send, self._ge.fq_op_spn[i])
            )
            header.grid(row=0,column=0)
            label.grid(row=i+1, column=0)
            freq_name.grid(row=0,column=1)
            self._ge.freq_label_freq[i].grid(row=i+1, column=1)
            duty_name.grid(row=0,column=2)
            self._ge.freq_label_duty[i].grid(row=i+1, column=2)
            self._ge.freq_button[i].grid(row=i+1, column=3)
            
            if self._ge.relay_bool_dict.get(self._ge.fq_op_spn[i]):
                self._ge.freq_op_option[i].grid(row=i+1,column=4)
            
            self._ge.freq_label_duty[i].insert(0, "0")
            self._ge.freq_label_freq[i].insert(0, "0")
      

    # Settings Tab
    def generate_setting_ui(self):
        
        #Settings container
        label_frame_setting = tk.LabelFrame(self._ge.setting_frame, text = "Settings")
        label_frame_setting.pack(expand="yes",fill="both")
        
        set_label = tk.Label(
            label_frame_setting,
            text="Set Slot Status: ",
            bg="azure3",
            width=30,
        )
        sn_label = tk.Label(
            label_frame_setting,
            text="Slot#: ",
            # bg="azure3",
            width=8,
        )
        st_label = tk.Label(
            label_frame_setting,
            text="Type: ",
            # bg="azure3",
            width=8,
        )
        board_label = tk.Label(
            label_frame_setting,
            text = "Board#: ",
            width=8,
        )
        self._ge.board_box = tk.Entry(
            label_frame_setting,
            bd=2,
            validate="key",
            width=6,
            font=("courier",10),
            textvariable="",
        )
        self._ge.slot_num_box = tk.Entry(
                label_frame_setting,
                bd=2,
                validate="key",
                width=6,
                font=("courier", 10),
                textvariable="",
        )
        self._ge.aux_box = tk.Entry(
                label_frame_setting,
                bd=2,
                validate="key",
                width=6,
                font=("courier", 10),
                textvariable="",
        )
        set_button = tk.Button(
                label_frame_setting,
                height=1,
                width=11,
                bd=8,
                fg="white",
                font=("Geneva", 6),
                text="Update",
                bg="Steel Blue",
                #command=partial(self.ui_call.freq_out_uc, i),
                command = partial(self._ec.set_slot)
        )
        set_label.grid(row=1,column=1)
        board_label.grid(row=1,column=2)
        self._ge.board_box.grid(row=1,column=3)
        sn_label.grid(row=1,column=4)
        self._ge.slot_num_box.grid(row=1,column=5)
        st_label.grid(row=1,column=6)
        self._ge.aux_box.grid(row=1,column=7)
        set_button.grid(row=1,column=8)
        
        reconnect_label = tk.Label(
            label_frame_setting,
            text="Reconnect to EtherCAT: ",
            bg="azure3",
            width=30,
        )
        reconnect_button = tk.Button(
                label_frame_setting,
                height=1,
                width=11,
                bd=8,
                fg="white",
                font=("Geneva", 6),
                text="Connect",
                bg="Steel Blue",
                #command=partial(self.ui_call.freq_out_uc, i),
                command = partial(self._ec.run_ec)
        )
        reconnect_label.grid(row=2,column=1)
        reconnect_button.grid(row=2,column=8)
        
        default_label = tk.Label(
            label_frame_setting,
            text="Reset slots to default types: ",
            bg="azure3",
            width=30,
        )
        default_button = tk.Button(
                label_frame_setting,
                height=1,
                width=11,
                bd=8,
                fg="white",
                font=("Geneva", 6),
                text="Reset",
                bg="Steel Blue",
                command = partial(self._ec.set_types)
        )
        default_label.grid(row=3,column=1)
        default_button.grid(row=3,column=8)
        