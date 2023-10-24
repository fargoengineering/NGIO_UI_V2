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

    def __init__(self, ob1):
        """
        Constructor used to create an instance of generate_ui.

        :param ob1 (Object): Used to pass an instance of global_defines.
        :param ob2 (Object): Used to pass an instance of IOCtrl.
        """
        self._ge = ob1
        self._ge.dig_ip_options = ["Open_Circuit"]
        self.ui_call = ui_callbacks(self._ge)


    # Generates first 7 UI Tabs
    def generate_spn_ui(self):
        """
        The function `generate_spn_ui` is responsible for creating these UI tabs and their widgets:

        DIG I/P | DIG O/P | VOL IN | VOL OUT | PWM IN | FREQ OUT
        """
        # Digital Input Tab
        for i in range(len(self._ge.dig_ip_spn)):
            self._ge.dig_ip_button.append(0)
            self._ge.dig_ip_option.append(0)
            self._ge.dig_ip_option_var.append(tk.StringVar())

            self._ge.dig_ip_button[i] = tk.Button(
                self._ge.dig_ip_frame,
                height=1,
                width=4,
                bd=6,
                fg="black",
                font=("Geneva", 6),
                bg="Green",
                command=partial(self.ui_call.dig_in_uc, i),
            )

            # self._ge.dig_ip_option[i] = tk.OptionMenu(
            #     self._ge.dig_ip_frame,
            #     self._ge.dig_ip_option_var[i],
            #     *self._ge.dig_ip_options,
            #     command=partial(self.ui_call.output_send, self._ge.dig_ip_spn[i])
            # )

            label = tk.Label(
                self._ge.dig_ip_frame,
                text=self._ge.dig_ip_name[i],
                bg="azure3",
                width=55,
            )

            self._ge.dig_ip_mode.update({i: 0})

            spn = self._ge.dig_ip_spn[i]
            # bno = self._ge.board_dict[spn]

            tempList = []
            # if bno in self._ge.board_wid_dict:
            #     tempList = self._ge.board_wid_dict[bno]

            tempList.append(self._ge.dig_ip_option[i])

            # self._ge.board_wid_dict.update({bno: tempList})

            # first column
            if i < 19:
                label.grid(row=i, column=0)
                self._ge.dig_ip_button[i].grid(row=i, column=1)
                # If Board and Channel are configured
                if self._ge.bool_both.get(self._ge.vol_ip_spn[i]):
                    self._ge.dig_ip_option[i].grid(row=i, column=2)
            # second column
            else:
                label.grid(row=i - 19, column=3)
                self._ge.dig_ip_button[i].grid(row=i - 19, column=4)
                # If Board and Channel are configured
                if self._ge.bool_both.get(self._ge.vol_ip_spn[i]):
                    self._ge.dig_ip_option[i].grid(row=i - 19, column=5)

        # Digital Output Tab
        for i in range(len(self._ge.dig_op_spn)):
            self._ge.dig_op_button.append(0)
            self._ge.dig_op_button[i] = tk.Button(
                self._ge.dig_op_frame,
                height=1,
                width=4,
                bd=6,
                fg="black",
                font=("Geneva", 6),
                bg="Green",
                command=partial(self.ui_call.dig_out_uc, i),
            )
            label = tk.Label(
                self._ge.dig_op_frame,
                text=self._ge.dig_op_name[i],
                bg="azure3",
                width=50,
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

        # Voltage In
        for i in range(len(self._ge.vol_ip_spn)):  # length = 58
            self._ge.volt_ip_label.append(0)
            self._ge.volt_ip_button.append(0)
            self._ge.volt_ip_toggle.append(0)
            self._ge.relay_switch.append(1)
            self._ge.volt_ip_string.append(tk.StringVar())
            label = tk.Label(
                self._ge.volt_ip_frame,
                text=self._ge.vol_ip_name[i],
                bg="azure3",
                width=55,
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

            if i < 29:
                label.grid(row=i, column=0)
                self._ge.volt_ip_label[i].grid(row=i, column=1)
                self._ge.volt_ip_button[i].grid(row=i, column=2)
                # If excel has board configured.
                if self._ge.bool_both.get(self._ge.vol_ip_spn[i]):
                    self._ge.volt_ip_toggle[i].grid(row=i, column=3)
            else:
                label.grid(row=i - 29, column=4)
                self._ge.volt_ip_label[i].grid(row=i - 29, column=5)
                self._ge.volt_ip_button[i].grid(row=i - 29, column=6)
                # If excel has board configured
                if self._ge.bool_both.get(self._ge.vol_ip_spn[i]):
                    self._ge.volt_ip_toggle[i].grid(row=i - 29, column=7)

            self._ge.volt_ip_label[i].insert(0, "0")
            
        # Voltage Out
        for i in range(len(self._ge.vol_op_spn)):  # length = 58
            self._ge.volt_op_label.append(0)
            self._ge.volt_op_button.append(0)
            self._ge.volt_op_toggle.append(0)
            self._ge.relay_switch.append(1)
            self._ge.volt_op_string.append(tk.StringVar())
            label = tk.Label(
                self._ge.volt_op_frame,
                text=self._ge.vol_op_name[i],
                bg="azure3",
                width=55,
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

            if i < 29:
                label.grid(row=i, column=0)
                self._ge.volt_op_label[i].grid(row=i, column=1)
                self._ge.volt_op_button[i].grid(row=i, column=2)
                # If excel has board configured.
                if self._ge.bool_both.get(self._ge.vol_op_spn[i]):
                    self._ge.volt_op_toggle[i].grid(row=i, column=3)
            else:
                label.grid(row=i - 29, column=4)
                self._ge.volt_op_label[i].grid(row=i - 29, column=5)
                self._ge.volt_op_button[i].grid(row=i - 29, column=6)
                # If excel has board configured
                if self._ge.bool_both.get(self._ge.vol_op_spn[i]):
                    self._ge.volt_op_toggle[i].grid(row=i - 29, column=7)

            self._ge.volt_op_label[i].insert(0, "0")
            
        # PWM Input Tab
        for i in range(len(self._ge.pwm_ip_spn)):
            self._ge.pwm_ip_label.append(0)
            self._ge.pwm_ip_button.append(0)
            self._ge.pwm_ip_toggle.append(0)
            self._ge.pwm_ip_string.append(tk.StringVar())
            label = tk.Label(
                self._ge.pwm_ip_frame,
                text=self._ge.pwm_ip_name[i],
                bg="azure3",
                width=55,
            )
            self._ge.pwm_ip_label[i] = tk.Entry(
                self._ge.pwm_ip_frame,
                bd=2,
                validate="key",
                width=6,
                font=("courier", 10),
                textvariable=self._ge.pwm_ip_string[i],
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
            label.grid(row=i, column=0)
            self._ge.pwm_ip_label[i].grid(row=i, column=1)
            self._ge.pwm_ip_button[i].grid(row=i, column=2)
            self._ge.pwm_ip_label[i].insert(0, "0")

            # Create a Button for toggling relay, based on excel configuration
            self._ge.pwm_ip_toggle[i] = tk.Button(
                self._ge.pwm_ip_frame,
                height=1,
                width=4,
                bd=6,
                fg="black",
                font=("Geneva", 6),
                bg="Green",
                command=partial(self.ui_call.pwm_in_uc, i),
            )
            if self._ge.bool_both.get(self._ge.pwm_ip_spn[i]):
                self._ge.pwm_ip_toggle[i].grid(row=i, column=3)


        # Freq Tab
        for i in range(len(self._ge.fq_op_spn)):
            self._ge.freq_label.append(0)
            self._ge.freq_button.append(0)
            self._ge.freq_toggle.append(0)
            self._ge.freq_string.append(tk.StringVar())
            label = tk.Label(
                self._ge.freq_op_frame,
                text=self._ge.fq_op_name[i],
                bg="azure3",
                width=55,
            )
            self._ge.freq_label[i] = tk.Entry(
                self._ge.freq_op_frame,
                bd=2,
                validate="key",
                width=6,
                font=("courier", 10),
                textvariable=self._ge.freq_string[i],
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
            label.grid(row=i, column=0)
            self._ge.freq_label[i].grid(row=i, column=1)
            self._ge.freq_button[i].grid(row=i, column=2)
            self._ge.freq_label[i].insert(0, "0")
            self._ge.freq_toggle[i] = tk.Button(
                self._ge.freq_op_frame,
                height=1,
                width=4,
                bd=6,
                fg="black",
                font=("Geneva", 6),
                bg="Green",
                command=partial(self.ui_call.freq_out_uc, i),
            )

            if self._ge.bool_both.get(self._ge.fq_op_spn[i]):
                self._ge.freq_toggle[i].grid(row=i, column=3)

    

    # Settings Tab
    def generate_setting_ui(self):

        # Settings Container
        label_frame_setting = tk.LabelFrame(self._ge.setting_frame, text="Setting")
        label_frame_setting.pack(expand="yes", fill="both")