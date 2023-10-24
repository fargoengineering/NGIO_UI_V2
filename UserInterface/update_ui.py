import itertools
import tkinter as tk
from tkinter import ttk
from functools import partial
import threading


class update_ui:

    global _ui, io_ob

    def __init__(self, ob1):
        """
        This module handles all updating of UI widgets and displayed values
        :param ob1: Set to _ui...references global_defines
        :param ob2: Set to io_ob...initially referenced IO_Ctrl(deprecated)
        """
        self._ui = ob1
        self.label_refresh_rate = 0

    def update_ui_dict(self):
        for key in self._ui.UI_dict:
            if self._ui.testing_active == 0:
                val = self.io_ob.data_read(key)
            else:
                if self._ui.toggle == 0:
                    val = 1
                else:
                    val = 0

            self._ui.UI_dict.update({key: val})
        if self._ui.testing_active == 1:
            if self._ui.toggle == 0:
                self._ui.toggle = 1
            else:
                self._ui.toggle = 0

        self.update_ui_spn()

    def update_ui_spn(self):
        """
        Function to update UI based on dictionary data.

        Tied to First 7 SPN Tabs.

        This is what causes the buttons to flash red and green in testing mode.
        """
        for key in self._ui.UI_dict:
            data = self._ui.UI_dict[key]

            try:
                # DIG I/P
                if key in self._ui.dig_ip_spn:
                    ind = self._ui.dig_ip_spn.index(key)
                    if self._ui.dig_state[key] == 1:
                        self._ui.dig_ip_button[ind].config(bg="Green")
                    else:
                        self._ui.dig_ip_button[ind].config(bg="Red")  # runtime error
                    i = ind
                    if i < 19:
                        self._ui.dig_ip_button[i].grid(row=i, column=1)
                    else:
                        self._ui.dig_ip_button[i].grid(row=i - 19, column=4)

                # DIG O/P
                elif key in self._ui.dig_op_spn:
                    ind = self._ui.dig_op_spn.index(key)  # find position of that spn
                    if data == 1:
                        self._ui.dig_op_button[ind].config(bg="Green")
                    else:
                        self._ui.dig_op_button[ind].config(bg="Red")
                    i = ind
                    if 0 <= i < 31:
                        row = i
                        column = 1
                    elif 31 <= i < 62:
                        row = i - 31
                        column = 3
                    elif 62 <= i < 94:
                        row = i - 62
                        column = 5
                    self._ui.dig_op_button[i].grid(row=row, column=column + 2)

                # Voltage In
                elif key in self._ui.vol_ip_spn:
                    ind = self._ui.vol_ip_spn.index(key)

                    i = ind
                    if i < 29:
                        self._ui.volt_in_label[i].grid(row=i, column=1)
                    else:
                        self._ui.volt_in_label[i].grid(row=i - 29, column=5)

                    if self._ui.SimMode == 1:
                        if self._ui.volt_in_state[key] == 1:
                            self._ui.volt_in_toggle[ind].config(bg="Green")
                        else:
                            self._ui.volt_in_toggle[ind].config(bg="Red")

                    self._ui.volt_in_label[ind].delete(0, 100)
                    self._ui.volt_in_label[ind].insert(0, data)
                
                # Voltage Out
                elif key in self._ui.vol_op_spn:
                    ind = self._ui.vol_op_spn.index(key)

                    i = ind
                    if i < 29:
                        self._ui.volt_op_label[i].grid(row=i, column=1)
                    else:
                        self._ui.volt_op_label[i].grid(row=i - 29, column=5)

                    if self._ui.SimMode == 1:
                        if self._ui.volt_op_state[key] == 1:
                            self._ui.volt_op_toggle[ind].config(bg="Green")
                        else:
                            self._ui.volt_op_toggle[ind].config(bg="Red")

                    self._ui.volt_op_label[ind].delete(0, 100)
                    self._ui.volt_op_label[ind].insert(0, data)

                # PWM In
                elif key in self._ui.pwm_ip_spn:
                    ind = self._ui.pwm_ip_spn.index(key)
                    self._ui.pwm_ip_label[ind].delete(0, 100)
                    self._ui.pwm_ip_label[ind].insert(0, data)
                    
                # Update Freq Tab
                elif key in self._ui.fq_op_spn:
                    ind = self._ui.fq_op_spn.index(key)
                    self._ui.freq_label[ind].delete(0, 100)
                    self._ui.freq_label[ind].insert(0, data)

                    if self._ui.SimMode == 1:
                        if self._ui.freq_state[key] == 1:
                            self._ui.freq_toggle[ind].config(bg="Green")
                        else:
                            self._ui.freq_toggle[ind].config(bg="Red")

            except RuntimeError as e:
                pass
                print(f"Runtime ERROR: {e}")
                


    def mainloop(self):
        """
        Holds Tkinter .mainloop()

        Main function for running UI.

        DO NOT REMOVE
        """
        tk.mainloop()
