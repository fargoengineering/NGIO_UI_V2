from global_defines import *
import pandas as pd
import os


class parse_excel:
    """
    This module is used to parse necessary data that has been configured in the Excel file: `Config_sheet.xlsx`

    Utilizes `pandas` python module to parse and read data from the CSV file, and converts said data into a pandas dataframe for manipulation.
    """

    global df, _pe

    def __init__(self, ob):
        """
        Module Initializing function.

        NOTE: may need to alter slash in path variable to match with OS file system...
        For windows, use backslash, for Unix, use forward slash.
        """
        path = os.path.dirname(__file__)
        path += "/Config_sheet.xlsx"
        # path += "/Config_sheet_old.xlsx"  #Legacy Config for backwards compatibility testing
        self.df = pd.read_excel(path, "SPN", header=1)
        self._pe = ob

    def parse_excel(self):
        """
        Opens the file specified by `path` variable, and parses data listed in SPN table.

        Tkinter will generate necessary components, based on the excel configuration.
        """
        for i in range(8):
            spn = i
            self._pe.spn_list.append(spn)
            spn_data = self.df.loc[i, "type"]
            spn_type = str(spn_data)

            # Check if 3 columns are configured:
            if (
                ("Board_Num" in self.df.columns)
                and ("Channel" in self.df.columns)
                and ("open_to" in self.df.columns)
            ):
                self._pe.fei_compatible = 1
            else:
                self._pe.fei_compatible = 0

            # Only if type column has valid entries
            if (
                (self._pe.dig_ip_str in spn_type)
                or (self._pe.dig_op_str in spn_type)
                or (self._pe.vol_ip_str in spn_type)
                or (self._pe.vol_op_str in spn_type)
                or (self._pe.pwm_ip_str in spn_type)
                or (self._pe.fq_op_str in spn_type)
            ):
                # required data
                name = self.df.loc[spn, "Name"]
                self._pe.name_list.append(name)
                self._pe.UI_spn.append(spn)
                self._pe.UI_dict.update({spn: 0})
                name_spn = "SPN" + str(spn)
                self._pe.config_dict.update({spn: name})  # all data in dictionary
              
                new_name = name_spn + " : " + name
                if self._pe.dig_ip_str in spn_type:
                    self._pe.dig_ip_spn.append(spn)
                    self._pe.dig_ip_name.append(new_name)
                    self._pe.type_dict.update({spn: "digin"})

                elif self._pe.dig_op_str in spn_type:
                    self._pe.dig_op_spn.append(spn)
                    self._pe.dig_op_name.append(new_name)
                    self._pe.type_dict.update({spn: "digout"})

                elif self._pe.vol_ip_str in spn_type:
                    self._pe.vol_ip_spn.append(spn)
                    self._pe.vol_ip_name.append(new_name)
                    self._pe.type_dict.update({spn: "voltin"})
                
                elif self._pe.vol_op_str in spn_type:
                    self._pe.vol_op_spn.append(spn)
                    self._pe.vol_op_name.append(new_name)
                    self._pe.type_dict.update({spn: "voltout"})

                elif self._pe.pwm_ip_str in spn_type:
                    self._pe.pwm_ip_spn.append(spn)
                    self._pe.pwm_ip_name.append(new_name)
                    self._pe.type_dict.update({spn: "pwmout"})

                elif self._pe.fq_op_str in spn_type:
                    self._pe.fq_op_spn.append(spn)
                    self._pe.fq_op_name.append(new_name)
                    self._pe.type_dict.update({spn: "freqout"})




